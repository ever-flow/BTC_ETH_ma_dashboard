"""
Configuration file for Crypto MA Strategy Analyzer
"""
import os
from datetime import datetime
from typing import Dict, List

class Config:
    """Application configuration"""

    # Data Configuration
    DATA_START_DATE = "2018-01-01"
    CRYPTO_SYMBOLS = ["BTC-USD", "ETH-USD"]

    # Strategy Configuration
    STRATEGIES = {
        'BTC_only': {
            'name': 'BTC 단일 투자',
            'description': 'Bitcoin 단일 투자 전략',
            'ma_range': (5, 100),
            'icon': '🟠'
        },
        'ETH_only': {
            'name': 'ETH 단일 투자', 
            'description': 'Ethereum 단일 투자 전략',
            'ma_range': (5, 100),
            'icon': '🔵'
        },
        'rebalance_50_50': {
            'name': '50:50 리밸런싱',
            'description': 'BTC:ETH = 50:50 리밸런싱 전략',
            'ma_range': (10, 60),
            'weights': [0.5, 0.5],
            'icon': '⚖️'
        },
        'rebalance_60_40': {
            'name': '60:40 리밸런싱',
            'description': 'BTC:ETH = 60:40 리밸런싱 전략', 
            'ma_range': (10, 60),
            'weights': [0.6, 0.4],
            'icon': '📊'
        }
    }

    # Optimization Configuration
    OPTIMIZATION = {
        'scoring_method': 'enhanced_sortino',  # enhanced_sortino, sharpe, cagr
        'time_weighting': {
            'recent_weight': 0.7,      # Weight for recent performance
            'historical_weight': 0.3   # Weight for historical performance
        },
        'recent_period_months': 24,    # Months for recent performance calculation
        'parallel_workers': 4,         # Number of parallel workers for optimization
        'timeout_per_ma': 30          # Timeout per MA calculation (seconds)
    }

    # Risk Management
    RISK_MANAGEMENT = {
        'max_drawdown_threshold': -0.6,  # -60%
        'volatility_threshold': 0.8,     # 80%
        'min_trades_per_year': 2,        # Minimum trades per year
        'signal_buffer': 0.02,           # 2% buffer for signal generation
        'risk_free_rate': 0.02           # 2% risk-free rate
    }

    # Signal Configuration
    SIGNALS = {
        'strong_buy_threshold': 1.02,    # 2% above MA
        'weak_buy_threshold': 1.0,       # Above MA
        'weak_sell_threshold': 1.0,      # Below MA  
        'strong_sell_threshold': 0.98,   # 2% below MA
        'confidence_multiplier': 1000    # For signal strength calculation
    }

    # Update Schedule
    UPDATE_SCHEDULE = {
        'update_time': "09:00",          # Daily update time (24h format)
        'timezone': "Asia/Seoul",         # Timezone
        'retry_attempts': 3,             # Number of retry attempts
        'retry_delay': 300               # Delay between retries (seconds)
    }

    # File Paths
    PATHS = {
        'data_file': 'strategy_results.json',
        'log_file': 'crypto_analyzer.log',
        'backup_dir': 'backups',
        'export_dir': 'exports'
    }

    # Streamlit Configuration
    STREAMLIT = {
        'page_title': '🚀 암호화폐 최적 이동평균 전략 분석',
        'page_icon': '🚀',
        'layout': 'wide',
        'cache_ttl': 3600,               # Cache TTL in seconds (1 hour)
        'theme': {
            'primary_color': '#667eea',
            'secondary_color': '#764ba2',
            'success_color': '#28a745',
            'warning_color': '#ffc107', 
            'danger_color': '#dc3545'
        }
    }

    # API Configuration (for future enhancements)
    API = {
        'rate_limit': 60,                # Requests per minute
        'timeout': 30,                   # Request timeout (seconds)
        'max_retries': 3,
        'backoff_factor': 2
    }

    # Notification Configuration
    NOTIFICATIONS = {
        'email': {
            'enabled': False,
            'smtp_server': '',
            'smtp_port': 587,
            'username': '',
            'password': '',
            'from_email': '',
            'to_emails': []
        },
        'webhook': {
            'enabled': False,
            'url': '',
            'headers': {}
        }
    }

    # Performance Thresholds
    PERFORMANCE_THRESHOLDS = {
        'excellent_cagr': 0.3,           # 30%
        'good_cagr': 0.2,                # 20%
        'acceptable_cagr': 0.1,          # 10%
        'excellent_sharpe': 2.0,
        'good_sharpe': 1.5,
        'acceptable_sharpe': 1.0,
        'max_acceptable_mdd': -0.5       # -50%
    }

    # UI Configuration
    UI = {
        'cards_per_row': 2,
        'chart_height': 400,
        'table_height': 300,
        'animation_duration': 500,
        'colors': {
            'buy': '#28a745',
            'sell': '#dc3545', 
            'hold': '#6c757d',
            'strong_buy': '#155724',
            'strong_sell': '#721c24'
        }
    }

    @classmethod
    def get_strategy_config(cls, strategy_name: str) -> Dict:
        """Get configuration for specific strategy"""
        return cls.STRATEGIES.get(strategy_name, {})

    @classmethod
    def get_ma_range(cls, strategy_name: str) -> tuple:
        """Get MA range for specific strategy"""
        config = cls.get_strategy_config(strategy_name)
        return config.get('ma_range', (5, 100))

    @classmethod
    def get_weights(cls, strategy_name: str) -> List[float]:
        """Get portfolio weights for strategy"""
        config = cls.get_strategy_config(strategy_name)
        return config.get('weights', [1.0])

    @classmethod
    def is_rebalancing_strategy(cls, strategy_name: str) -> bool:
        """Check if strategy is a rebalancing strategy"""
        return strategy_name.startswith('rebalance_')

    @classmethod
    def get_risk_level(cls, sharpe_ratio: float, max_drawdown: float) -> str:
        """Determine risk level based on metrics"""
        if sharpe_ratio >= 2.0 and max_drawdown >= -0.3:
            return "낮음"
        elif sharpe_ratio >= 1.5 and max_drawdown >= -0.4:
            return "보통"
        elif sharpe_ratio >= 1.0 and max_drawdown >= -0.5:
            return "높음"
        else:
            return "매우 높음"

    @classmethod
    def get_performance_grade(cls, cagr: float) -> str:
        """Get performance grade based on CAGR"""
        if cagr >= cls.PERFORMANCE_THRESHOLDS['excellent_cagr']:
            return "우수"
        elif cagr >= cls.PERFORMANCE_THRESHOLDS['good_cagr']:
            return "좋음"
        elif cagr >= cls.PERFORMANCE_THRESHOLDS['acceptable_cagr']:
            return "보통"
        else:
            return "개선 필요"

# Environment Variables (for production deployment)
class ProductionConfig(Config):
    """Production configuration with environment variables"""

    # Override with environment variables if available
    DATA_START_DATE = os.getenv('DATA_START_DATE', Config.DATA_START_DATE)

    # Database configuration (for future use)
    DATABASE_URL = os.getenv('DATABASE_URL', '')

    # Redis configuration (for caching)
    REDIS_URL = os.getenv('REDIS_URL', '')

    # Email configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', '')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')

    # Webhook configuration
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

    @classmethod
    def setup_production_logging(cls):
        """Setup production logging configuration"""
        import logging.config

        LOGGING_CONFIG = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': {
                'default': {
                    'level': 'INFO',
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                },
                'file': {
                    'level': 'INFO',
                    'formatter': 'standard',
                    'class': 'logging.FileHandler',
                    'filename': cls.PATHS['log_file'],
                    'mode': 'a',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['default', 'file'],
                    'level': 'INFO',
                    'propagate': False
                }
            }
        }

        logging.config.dictConfig(LOGGING_CONFIG)

# Development configuration
class DevelopmentConfig(Config):
    """Development configuration"""

    # Reduced data for faster testing
    DATA_START_DATE = "2022-01-01"

    # Faster optimization for development
    OPTIMIZATION = {
        **Config.OPTIMIZATION,
        'parallel_workers': 2,
        'timeout_per_ma': 10
    }

    # More frequent updates for testing
    UPDATE_SCHEDULE = {
        **Config.UPDATE_SCHEDULE,
        'update_time': "*/5 * * * *"  # Every 5 minutes (cron format)
    }

# Get configuration based on environment
def get_config():
    """Get configuration based on environment"""
    env = os.getenv('ENVIRONMENT', 'development').lower()

    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()
