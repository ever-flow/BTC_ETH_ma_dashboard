# 🚀 암호화폐 최적 이동평균 전략 분석기

실시간 데이터 기반으로 BTC, ETH의 최적 이동평균 전략을 분석하고 매매 신호를 제공하는 웹 애플리케이션입니다.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## ✨ 주요 기능

### 📊 4가지 투자 전략 분석
- **🟠 BTC 단일 투자**: Bitcoin 단독 투자 전략
- **🔵 ETH 단일 투자**: Ethereum 단독 투자 전략
- **⚖️ 50:50 리밸런싱**: BTC:ETH = 50:50 포트폴리오
- **📊 60:40 리밸런싱**: BTC:ETH = 60:40 포트폴리오

### 🎯 고도화된 최적화 알고리즘
- **시간 감쇠 가중치**: 최근 데이터에 더 높은 가중치
- **변동성 조정**: 시장 변동성에 따른 적응형 가중치
- **성과 기반 가중치**: 최근 성과를 반영한 동적 조정

### 📈 실시간 매매 신호
- **현재 포지션 상태**: 매수/매도/현금보유 신호
- **신호 강도**: 신뢰도 기반 신호 세기 표시
- **신호 지속 기간**: 현재 신호 유지 기간
- **다음 신호 예측**: 신호 변경 가능성 분석

### 🎨 인터랙티브 대시보드
- **실시간 성과 비교**: 전략별 상세 성과 매트릭스
- **시각적 차트**: Plotly 기반 고급 인터랙티브 차트
- **위험도 분석**: 실시간 위험 지표 및 히트맵
- **시장 상황 분석**: 현재 시장 트렌드 및 변동성 지수

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/crypto-strategy-analyzer.git
cd crypto-strategy-analyzer
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 초기 분석 실행
```bash
python data_processor.py
```

### 4. 웹 애플리케이션 시작
```bash
streamlit run enhanced_app.py
```

애플리케이션이 `http://localhost:8501`에서 실행됩니다.

## 🐳 Docker로 실행

### 간단한 실행
```bash
docker build -t crypto-analyzer .
docker run -p 8501:8501 crypto-analyzer
```

### Docker Compose로 실행
```bash
# 기본 실행
docker-compose up -d

# 스케줄러 포함 실행
docker-compose --profile with-scheduler up -d

# 전체 스택 (Redis, PostgreSQL 포함)
docker-compose --profile with-redis --profile with-db --profile with-scheduler up -d
```

## ☁️ 클라우드 배포

### Streamlit Cloud
1. GitHub에 저장소 업로드
2. [share.streamlit.io](https://share.streamlit.io)에서 배포
3. 자동 업데이트는 GitHub Actions를 통해 실행

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku addons:create scheduler:standard
```

### GitHub Pages + Actions
- GitHub Pages 활성화
- GitHub Actions가 매일 자동 업데이트 실행
- 정적 사이트와 Streamlit 앱 연동

자세한 배포 방법은 [배포 가이드](deploy_guide.md)를 참조하세요.

## ⏰ 자동 업데이트

### 스케줄러 설정
```bash
# 로컬 스케줄러 실행
python scheduler.py --platform=local

# 한 번만 실행
python scheduler.py --once

# Cron 엔트리 생성
python scheduler.py --create-cron
```

### 플랫폼별 자동 업데이트
- **Heroku**: Heroku Scheduler 애드온 사용
- **GitHub Actions**: 매일 오전 9시(KST) 자동 실행
- **Linux Cron**: crontab을 통한 스케줄링
- **Streamlit Cloud**: GitHub Actions 연동

## 📊 성과 지표

### 주요 메트릭
- **CAGR (연평균 수익률)**: 복리 기준 연평균 수익률
- **MDD (최대 낙폭)**: 최대 손실 구간
- **Sharpe Ratio**: 위험 대비 수익률
- **Sortino Ratio**: 하방 위험 기준 수익률
- **Combined Score**: 시간 가중 통합 점수

### 위험 관리
- **신호 버퍼**: 2% 버퍼로 잦은 거래 방지
- **변동성 임계값**: 시장 변동성 모니터링
- **최대 낙폭 제한**: 위험 수준 경고 시스템

## 🔧 설정 및 커스터마이징

### 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env
```

주요 설정:
- `DATA_START_DATE`: 분석 시작 날짜
- `ENVIRONMENT`: 실행 환경 (development/production)
- 이메일/웹훅 알림 설정

### 전략 파라미터 조정
`config.py`에서 다음 설정 조정 가능:
- MA 범위 설정
- 최적화 가중치
- 신호 생성 임계값
- 위험 관리 파라미터

## 📈 사용 예시

### 현재 매매 신호 확인
```python
from data_processor import CryptoStrategyAnalyzer

analyzer = CryptoStrategyAnalyzer()
results = analyzer.run_full_analysis()

for strategy, data in results.items():
    if strategy != 'metadata':
        print(f"{data['strategy_name']}: {data['current_signal']}")
```

### 백테스팅 결과 분석
```python
# 특정 전략의 상세 분석
btc_result = results['BTC_only']
print(f"최적 MA: {btc_result['optimal_ma']}일")
print(f"CAGR: {btc_result['cagr']:.2f}%")
print(f"MDD: {btc_result['mdd']:.2f}%")
```

## 📚 문서

- [배포 가이드](deploy_guide.md): 상세한 배포 방법
- [API 문서](docs/api.md): 코드 API 참조
- [설정 가이드](docs/configuration.md): 상세 설정 방법
- [FAQ](docs/faq.md): 자주 묻는 질문

## 🔍 개발자 도구

### 로컬 개발 헬퍼
```bash
# 개발 환경 설정
python run_local.py setup

# 분석 실행
python run_local.py analysis

# 앱 시작
python run_local.py app

# 테스트 실행
python run_local.py test

# 전체 검증
python run_local.py all
```

### 테스트
```bash
pytest tests/ -v --cov=.
```

### 코드 품질
```bash
black . --check
flake8 .
```

## 📊 시스템 요구사항

### 최소 요구사항
- Python 3.9+
- RAM: 1GB+
- 디스크: 500MB+
- 인터넷 연결 (데이터 수집)

### 권장 사양
- Python 3.11+
- RAM: 2GB+
- 디스크: 1GB+
- SSD 저장장치

## ⚠️ 주의사항

### 투자 관련
- **본 서비스는 투자 참고용으로만 사용하세요**
- **투자 결정은 본인의 판단과 책임하에 이루어져야 합니다**
- **과거 성과가 미래 수익을 보장하지 않습니다**

### 기술적 제한
- 데이터는 yfinance API에 의존
- 실시간 데이터는 15-20분 지연 가능
- 백테스팅 결과는 수수료 미포함

## 🤝 기여하기

### 버그 리포트
[GitHub Issues](https://github.com/your-username/crypto-strategy-analyzer/issues)를 통해 버그를 신고해주세요.

### 기능 제안
새로운 기능 아이디어가 있으시면 Issue를 생성해주세요.

### 코드 기여
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 지원

- **GitHub Issues**: [이슈 페이지](https://github.com/your-username/crypto-strategy-analyzer/issues)
- **이메일**: your-email@example.com
- **위키**: [프로젝트 위키](https://github.com/your-username/crypto-strategy-analyzer/wiki)

## 🙏 감사의 말

- [yfinance](https://github.com/ranaroussi/yfinance) - 금융 데이터 제공
- [Streamlit](https://streamlit.io/) - 웹 애플리케이션 프레임워크
- [Plotly](https://plotly.com/) - 인터랙티브 차트
- [pandas](https://pandas.pydata.org/) - 데이터 분석 라이브러리

---

**⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!**

**📈 투자에 성공하시길 바랍니다!**
