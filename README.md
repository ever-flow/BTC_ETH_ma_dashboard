# 🚀 암호화폐 최적 이동평균 전략 분석기

BTC와 ETH의 과거 가격 데이터를 활용해 이동평균 기반 투자 전략을 분석하고 시각화하는 Streamlit 대시보드입니다. 데이터 수집부터 전략 최적화, 신호 표시까지 하나의 파이프라인으로 구성되어 있습니다.

## 주요 기능
- BTC/ETH 단일 전략과 포트폴리오 전략 성과 비교
- 변동성 및 최근 성과를 반영한 최적 이동평균 탐색
- 실시간 매매 신호와 인터랙티브 차트 제공

## 프로젝트 구조
- `config.py`: 전략, 리스크 관리 및 Streamlit 설정을 포함한 중앙 구성 파일
- `data_processor.py`: 야후 파이낸스 데이터를 기반으로 이동평균 전략을 백테스트하고 `strategy_results.json`에 결과 저장
- `enhanced_app.py`: 분석 결과와 매매 신호를 표시하는 Streamlit 대시보드
- `requirements.txt`: 애플리케이션 실행에 필요한 Python 패키지 목록

## 빠른 시작
```bash
git clone https://github.com/your-username/crypto-strategy-analyzer.git
cd crypto-strategy-analyzer
pip install -r requirements.txt
python data_processor.py  # 초기 데이터 분석
streamlit run enhanced_app.py
```

애플리케이션은 기본적으로 `http://localhost:8501`에서 실행됩니다.

## 라이선스

이 프로젝트는 MIT 라이선스로 배포됩니다.
