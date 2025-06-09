"""
Automatic scheduler for crypto strategy analysis updates
Supports multiple deployment platforms and scheduling methods
"""

import schedule
import time
import logging
import datetime
import sys
import os
from pathlib import Path
import subprocess
import json
from typing import Optional, Dict, Any
import traceback
import requests

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor import CryptoStrategyAnalyzer
from config import get_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CryptoAnalysisScheduler:
    """Automatic scheduler for crypto analysis updates"""

    def __init__(self):
        self.config = get_config()
        self.analyzer = CryptoStrategyAnalyzer()
        self.last_update = None
        self.update_count = 0
        self.error_count = 0
        self.max_errors = 5

    def run_analysis(self) -> bool:
        """Run the crypto analysis and save results"""
        try:
            logger.info("🚀 암호화폐 전략 분석 시작")
            start_time = datetime.datetime.now()

            # Run analysis
            results = self.analyzer.run_full_analysis()

            if not results:
                raise Exception("분석 결과가 비어있습니다")

            # Save results
            self.analyzer.save_results(results)

            # Update statistics
            self.last_update = datetime.datetime.now()
            self.update_count += 1
            self.error_count = 0  # Reset error count on success

            # Calculate duration
            duration = (datetime.datetime.now() - start_time).total_seconds()

            # Log success
            logger.info(f"✅ 분석 완료 (소요시간: {duration:.2f}초)")

            # Send notification if configured
            self._send_notification(
                title="분석 완료",
                message=f"암호화폐 전략 분석이 성공적으로 완료되었습니다. (업데이트 #{self.update_count})",
                data=results.get('metadata', {})
            )

            return True

        except Exception as e:
            self.error_count += 1
            error_msg = f"분석 실패 (오류 #{self.error_count}): {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())

            # Send error notification
            self._send_notification(
                title="분석 실패",
                message=error_msg,
                is_error=True
            )

            # Stop scheduler if too many errors
            if self.error_count >= self.max_errors:
                logger.critical(f"연속 오류 {self.max_errors}회 발생. 스케줄러를 중단합니다.")
                return False

            return True  # Continue despite error

    def _send_notification(self, title: str, message: str, data: Dict = None, is_error: bool = False):
        """Send notification via configured channels"""
        try:
            # Email notification
            if self.config.NOTIFICATIONS['email']['enabled']:
                self._send_email_notification(title, message, data, is_error)

            # Webhook notification
            if self.config.NOTIFICATIONS['webhook']['enabled']:
                self._send_webhook_notification(title, message, data, is_error)

        except Exception as e:
            logger.warning(f"알림 전송 실패: {e}")

    def _send_email_notification(self, title: str, message: str, data: Dict = None, is_error: bool = False):
        """Send email notification"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            email_config = self.config.NOTIFICATIONS['email']

            msg = MIMEMultipart()
            msg['From'] = email_config['from_email']
            msg['To'] = ', '.join(email_config['to_emails'])
            msg['Subject'] = f"[암호화폐 분석] {title}"

            body = f"""
            {message}

            시간: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            총 업데이트 횟수: {self.update_count}
            연속 오류 횟수: {self.error_count}

            {json.dumps(data, ensure_ascii=False, indent=2) if data else ''}
            """

            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['username'], email_config['password'])
            server.send_message(msg)
            server.quit()

            logger.info("이메일 알림 전송 완료")

        except Exception as e:
            logger.error(f"이메일 전송 실패: {e}")

    def _send_webhook_notification(self, title: str, message: str, data: Dict = None, is_error: bool = False):
        """Send webhook notification"""
        try:
            webhook_config = self.config.NOTIFICATIONS['webhook']

            payload = {
                'title': title,
                'message': message,
                'timestamp': datetime.datetime.now().isoformat(),
                'update_count': self.update_count,
                'error_count': self.error_count,
                'is_error': is_error,
                'data': data or {}
            }

            response = requests.post(
                webhook_config['url'],
                json=payload,
                headers=webhook_config.get('headers', {}),
                timeout=30
            )

            response.raise_for_status()
            logger.info("웹훅 알림 전송 완료")

        except Exception as e:
            logger.error(f"웹훅 전송 실패: {e}")

    def health_check(self) -> Dict[str, Any]:
        """Return scheduler health status"""
        return {
            'status': 'running',
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'update_count': self.update_count,
            'error_count': self.error_count,
            'next_update': self._get_next_update_time(),
            'uptime': datetime.datetime.now().isoformat()
        }

    def _get_next_update_time(self) -> Optional[str]:
        """Get next scheduled update time"""
        try:
            next_job = schedule.next_run()
            return next_job.isoformat() if next_job else None
        except:
            return None

    def setup_schedule(self):
        """Setup the update schedule"""
        update_time = self.config.UPDATE_SCHEDULE['update_time']

        # Schedule daily update
        schedule.every().day.at(update_time).do(self.run_analysis)

        # Optional: Add additional schedules
        # schedule.every().hour.do(self.health_check)  # Hourly health check

        logger.info(f"스케줄 설정 완료: 매일 {update_time}에 업데이트")

    def run_scheduler(self):
        """Run the scheduler main loop"""
        logger.info("암호화폐 분석 스케줄러 시작")

        # Setup schedule
        self.setup_schedule()

        # Run initial analysis
        if not self.run_analysis():
            logger.critical("초기 분석 실패로 스케줄러를 종료합니다")
            return

        # Main scheduler loop
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute

        except KeyboardInterrupt:
            logger.info("스케줄러가 사용자에 의해 중단되었습니다")
        except Exception as e:
            logger.error(f"스케줄러 오류: {e}")
            logger.error(traceback.format_exc())
        finally:
            logger.info("스케줄러 종료")

class HerokuScheduler(CryptoAnalysisScheduler):
    """Heroku-specific scheduler using Heroku Scheduler add-on"""

    def run_once(self):
        """Run analysis once (for Heroku Scheduler)"""
        logger.info("Heroku 스케줄러로 실행")
        return self.run_analysis()

class GitHubActionsScheduler(CryptoAnalysisScheduler):
    """GitHub Actions scheduler"""

    def run_once(self):
        """Run analysis once (for GitHub Actions)"""
        logger.info("GitHub Actions로 실행")
        success = self.run_analysis()

        # Set GitHub Actions output
        if os.getenv('GITHUB_ACTIONS'):
            print(f"::set-output name=success::{success}")

        return success

class StreamlitCloudScheduler(CryptoAnalysisScheduler):
    """Streamlit Cloud scheduler using cron-like scheduling"""

    def __init__(self):
        super().__init__()
        self.last_check = datetime.datetime.now()

    def should_update(self) -> bool:
        """Check if it's time to update"""
        now = datetime.datetime.now()

        # Check if it's past the update time and we haven't updated today
        update_time = datetime.datetime.strptime(self.config.UPDATE_SCHEDULE['update_time'], '%H:%M').time()

        if (now.time() >= update_time and 
            (self.last_update is None or self.last_update.date() < now.date())):
            return True

        return False

    def check_and_update(self):
        """Check if update is needed and run if necessary"""
        if self.should_update():
            return self.run_analysis()
        return True

def create_cron_entry():
    """Create cron entry for Linux systems"""
    cron_command = f"0 9 * * * cd {os.getcwd()} && python scheduler.py --platform=cron"

    cron_entry = f"""# Crypto Strategy Analysis Auto Update
{cron_command}
"""

    with open('crontab_entry.txt', 'w') as f:
        f.write(cron_entry)

    print("Cron entry created: crontab_entry.txt")
    print("To install: crontab crontab_entry.txt")

def main():
    """Main function with platform detection"""
    import argparse

    parser = argparse.ArgumentParser(description='Crypto Strategy Analysis Scheduler')
    parser.add_argument('--platform', choices=['local', 'heroku', 'github', 'streamlit', 'cron'], 
                       default='local', help='Deployment platform')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--create-cron', action='store_true', help='Create cron entry file')

    args = parser.parse_args()

    if args.create_cron:
        create_cron_entry()
        return

    # Select appropriate scheduler
    if args.platform == 'heroku':
        scheduler = HerokuScheduler()
    elif args.platform == 'github':
        scheduler = GitHubActionsScheduler()
    elif args.platform == 'streamlit':
        scheduler = StreamlitCloudScheduler()
    else:
        scheduler = CryptoAnalysisScheduler()

    # Run once or start scheduler
    if args.once or args.platform in ['heroku', 'github']:
        success = scheduler.run_once()
        sys.exit(0 if success else 1)
    else:
        scheduler.run_scheduler()

if __name__ == "__main__":
    main()
