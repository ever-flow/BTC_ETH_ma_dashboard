# 🚀 암호화폐 이동평균 전략 분석기 배포 가이드

이 가이드는 암호화폐 이동평균 전략 분석 웹앱을 다양한 플랫폼에 배포하는 방법을 설명합니다.

## 📋 목차

1. [로컬 개발 환경 설정](#로컬-개발-환경-설정)
2. [Streamlit Cloud 배포](#streamlit-cloud-배포)
3. [Heroku 배포](#heroku-배포)
4. [GitHub Pages + Actions 배포](#github-pages--actions-배포)
5. [Docker 컨테이너 배포](#docker-컨테이너-배포)
6. [자동 업데이트 설정](#자동-업데이트-설정)
7. [환경 변수 설정](#환경-변수-설정)
8. [문제 해결](#문제-해결)

---

## 🖥️ 로컬 개발 환경 설정

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/crypto-strategy-analyzer.git
cd crypto-strategy-analyzer
```

### 2. 가상환경 생성 및 활성화
```bash
# Python 가상환경 생성
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 초기 데이터 생성
```bash
python data_processor.py
```

### 5. 애플리케이션 실행
```bash
streamlit run enhanced_app.py
```

애플리케이션이 `http://localhost:8501`에서 실행됩니다.

---

## ☁️ Streamlit Cloud 배포

### 1. GitHub 저장소 준비
- GitHub에 저장소 생성 및 코드 업로드
- `strategy_results.json` 파일이 저장소에 포함되어 있는지 확인

### 2. Streamlit Cloud 설정
1. [share.streamlit.io](https://share.streamlit.io) 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 저장소 선택: `your-username/crypto-strategy-analyzer`
5. Main file path: `enhanced_app.py`
6. "Deploy!" 클릭

### 3. 자동 업데이트 설정
Streamlit Cloud에서는 GitHub Actions를 통한 자동 업데이트를 사용합니다:

```bash
# GitHub Secrets 설정 (선택사항)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### 4. 배포 확인
- 배포 완료 후 제공되는 URL로 접속
- 예: `https://your-app-name.streamlit.app`

---

## 🟣 Heroku 배포

### 1. Heroku CLI 설치
[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) 설치

### 2. Heroku 애플리케이션 생성
```bash
# Heroku 로그인
heroku login

# 앱 생성
heroku create your-crypto-analyzer

# Git 원격 저장소 추가
heroku git:remote -a your-crypto-analyzer
```

### 3. 설정 파일 추가

**Procfile** 생성:
```bash
echo "web: streamlit run enhanced_app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
```

**runtime.txt** 생성:
```bash
echo "python-3.11.6" > runtime.txt
```

### 4. 환경 변수 설정
```bash
heroku config:set ENVIRONMENT=production
heroku config:set DATA_START_DATE=2018-01-01
```

### 5. 배포
```bash
git add .
git commit -m "Initial Heroku deployment"
git push heroku main
```

### 6. Heroku Scheduler 설정
```bash
# Scheduler 애드온 추가
heroku addons:create scheduler:standard

# 스케줄러 설정
heroku addons:open scheduler
```

스케줄러에서 다음 작업 추가:
- Command: `python scheduler.py --platform=heroku --once`
- Frequency: Daily at 9:00 AM

---

## 🐙 GitHub Pages + Actions 배포

### 1. GitHub Pages 활성화
1. GitHub 저장소 → Settings
2. Pages 섹션으로 이동
3. Source: "GitHub Actions" 선택

### 2. Secrets 설정
Repository Settings → Secrets and variables → Actions:

```
DOCKERHUB_USERNAME=your-dockerhub-username
DOCKERHUB_TOKEN=your-dockerhub-token
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
WEBHOOK_URL=https://hooks.slack.com/your-webhook-url
```

### 3. 워크플로우 활성화
- `.github/workflows/update.yml` 파일이 이미 포함되어 있음
- 코드를 main 브랜치에 푸시하면 자동으로 실행됨

### 4. 매일 자동 업데이트
- GitHub Actions가 매일 오전 9시(KST)에 자동 실행
- 분석 결과가 자동으로 업데이트됨

---

## 🐳 Docker 컨테이너 배포

### 1. Docker 이미지 빌드
```bash
docker build -t crypto-strategy-analyzer .
```

### 2. 로컬 실행
```bash
docker run -p 8501:8501 crypto-strategy-analyzer
```

### 3. Docker Hub에 푸시
```bash
# 태그 설정
docker tag crypto-strategy-analyzer your-username/crypto-strategy-analyzer:latest

# 로그인 및 푸시
docker login
docker push your-username/crypto-strategy-analyzer:latest
```

### 4. 클라우드 플랫폼 배포

#### AWS ECS
```bash
# ECS 클러스터 생성 및 서비스 배포
aws ecs create-cluster --cluster-name crypto-analyzer
# ... (상세한 ECS 설정)
```

#### Google Cloud Run
```bash
gcloud run deploy crypto-analyzer \
  --image your-username/crypto-strategy-analyzer:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name crypto-analyzer \
  --image your-username/crypto-strategy-analyzer:latest \
  --ports 8501
```

---

## ⏰ 자동 업데이트 설정

### 1. 플랫폼별 설정

#### Linux Cron
```bash
# crontab 엔트리 생성
python scheduler.py --create-cron

# cron 설치
crontab crontab_entry.txt
```

#### Windows Task Scheduler
1. Task Scheduler 열기
2. "Create Basic Task" 선택
3. 이름: "Crypto Analysis Update"
4. Trigger: Daily, 9:00 AM
5. Action: Start a program
6. Program: `python`
7. Arguments: `scheduler.py --platform=local --once`

### 2. 알림 설정

#### 이메일 알림
`config.py`에서 이메일 설정:
```python
NOTIFICATIONS = {
    'email': {
        'enabled': True,
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': 'your-email@gmail.com',
        'password': 'your-app-password',
        'from_email': 'your-email@gmail.com',
        'to_emails': ['recipient@gmail.com']
    }
}
```

#### Slack/Discord 웹훅
```python
NOTIFICATIONS = {
    'webhook': {
        'enabled': True,
        'url': 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK',
        'headers': {'Content-Type': 'application/json'}
    }
}
```

---

## 🔧 환경 변수 설정

### 필수 환경 변수
```bash
ENVIRONMENT=production
DATA_START_DATE=2018-01-01
```

### 선택적 환경 변수
```bash
# 이메일 설정
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# 웹훅 설정
WEBHOOK_URL=https://hooks.slack.com/your-webhook

# 데이터베이스 (향후 확장용)
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379

# 보안
SECRET_KEY=your-secret-key-here
```

### .env 파일 생성 (로컬 개발용)
```bash
# .env 파일 생성
cat > .env << 'EOF'
ENVIRONMENT=development
DATA_START_DATE=2022-01-01
SMTP_SERVER=smtp.gmail.com
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EOF
```

---

## 🔍 문제 해결

### 일반적인 문제들

#### 1. 메모리 부족 오류
```bash
# 해결방법: 더 적은 데이터로 시작
export DATA_START_DATE=2022-01-01
```

#### 2. API 요청 제한
```bash
# yfinance 요청 간격 조정
# data_processor.py에서 time.sleep() 추가
```

#### 3. Streamlit 포트 충돌
```bash
# 다른 포트 사용
streamlit run enhanced_app.py --server.port=8502
```

#### 4. Docker 빌드 실패
```bash
# 캐시 없이 빌드
docker build --no-cache -t crypto-strategy-analyzer .
```

### 로그 확인 방법

#### 로컬 환경
```bash
# 애플리케이션 로그
tail -f crypto_analyzer.log

# 스케줄러 로그
tail -f scheduler.log
```

#### Heroku
```bash
heroku logs --tail
```

#### Docker
```bash
docker logs container-name
```

### 성능 최적화

#### 1. 캐싱 활용
```python
# Streamlit 캐시 사용
@st.cache_data(ttl=3600)
def load_data():
    # 데이터 로딩 로직
```

#### 2. 데이터 샘플링
```python
# 큰 데이터셋의 경우 샘플링
if len(data) > 10000:
    data = data.sample(n=5000)
```

#### 3. 병렬 처리
```python
# 멀티프로세싱 사용
from concurrent.futures import ProcessPoolExecutor
```

---

## 📈 모니터링 및 유지보수

### 1. 헬스 체크 엔드포인트
Streamlit 앱에 헬스 체크 추가:
```python
# enhanced_app.py에 추가
if st.sidebar.button("Health Check"):
    health_status = scheduler.health_check()
    st.json(health_status)
```

### 2. 로그 모니터링
```bash
# 로그 로테이션 설정 (Linux)
sudo nano /etc/logrotate.d/crypto-analyzer
```

### 3. 백업 설정
```bash
# 일일 백업 스크립트
#!/bin/bash
cp strategy_results.json backups/strategy_results_$(date +%Y%m%d).json
```

---

## 🆘 지원 및 문의

- **GitHub Issues**: [프로젝트 이슈 페이지](https://github.com/your-username/crypto-strategy-analyzer/issues)
- **문서**: [프로젝트 Wiki](https://github.com/your-username/crypto-strategy-analyzer/wiki)
- **이메일**: your-email@example.com

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

## 🙏 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**마지막 업데이트**: 2024년 1월
**버전**: 2.0.0
