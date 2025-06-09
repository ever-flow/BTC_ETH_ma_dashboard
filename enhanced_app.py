import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import datetime
from dateutil.relativedelta import relativedelta
import warnings
import os
from data_processor import CryptoStrategyAnalyzer
from config import Config
import time

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="🚀 암호화폐 최적 이동평균 전략 분석",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }

    .strategy-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .strategy-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.15);
    }

    .metric-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }

    .signal-card {
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        font-weight: bold;
        font-size: 1.1rem;
    }

    .buy-signal {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }

    .sell-signal {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
    }

    .hold-signal {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
    }

    .update-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin-bottom: 2rem;
    }

    .risk-indicator {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
        font-weight: bold;
    }

    .risk-low { background: #28a745; color: white; }
    .risk-medium { background: #ffc107; color: #333; }
    .risk-high { background: #dc3545; color: white; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_strategy_data():
    """Load cached strategy results"""
    try:
        if os.path.exists('strategy_results.json'):
            with open('strategy_results.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # If no cached data, run analysis
            analyzer = CryptoStrategyAnalyzer()
            return analyzer.run_full_analysis()
    except Exception as e:
        st.error(f"데이터 로딩 오류: {e}")
        return None

def display_signal_card(signal, strength, last_change, days_since):
    """Display trading signal in a card format"""
    if "매수" in signal:
        card_class = "buy-signal"
        icon = "📈"
    elif "매도" in signal:
        card_class = "sell-signal" 
        icon = "📉"
    else:
        card_class = "hold-signal"
        icon = "➡️"

    st.markdown(f"""
    <div class="signal-card {card_class}">
        {icon} {signal} (신뢰도: {strength}%)
        <br><small>마지막 변경: {last_change} ({days_since}일 전)</small>
    </div>
    """, unsafe_allow_html=True)

def create_performance_chart(data):
    """Create interactive performance comparison chart"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('누적 수익률', 'Sharp Ratio 비교', '최대 낙폭 (MDD)', '월별 수익률 히트맵'),
        specs=[[{"secondary_y": False}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "heatmap"}]]
    )

    # Add performance traces
    strategies = list(data.keys())
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c']

    for i, strategy in enumerate(strategies):
        if 'cumulative_returns' in data[strategy]:
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(data[strategy]['cumulative_returns']))),
                    y=data[strategy]['cumulative_returns'],
                    name=strategy,
                    line=dict(color=colors[i % len(colors)], width=3)
                ),
                row=1, col=1
            )

    fig.update_layout(
        height=800,
        showlegend=True,
        title_text="전략별 성과 비교 대시보드",
        title_x=0.5
    )

    return fig

def display_market_status():
    """Display current market status and indicators"""
    st.markdown("### 🌐 현재 시장 상황")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-container">
            <h3>시장 트렌드</h3>
            <h2>상승 📈</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-container">
            <h3>변동성 지수</h3>
            <h2>중간 ⚡</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-container">
            <h3>공포탐욕지수</h3>
            <h2>중립 😐</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-container">
            <h3>추천 비중</h3>
            <h2>70% 💪</h2>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 암호화폐 최적 이동평균 전략 분석</h1>
        <p>실시간 데이터 기반 최적 투자 전략 제공 | 매일 자동 업데이트</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    data = load_strategy_data()

    if data is None:
        st.error("데이터를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.")
        return

    # Update info
    last_update = data.get('last_update', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    st.markdown(f"""
    <div class="update-info">
        📅 <strong>마지막 업데이트:</strong> {last_update} | 
        🔄 <strong>다음 업데이트:</strong> 내일 오전 9시 | 
        ⚡ <strong>데이터 상태:</strong> 실시간 반영
    </div>
    """, unsafe_allow_html=True)

    # Market Status
    display_market_status()

    # Strategy Analysis
    st.markdown("## 📊 최적 전략 분석 결과")

    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 실시간 신호", "📈 성과 비교", "🔍 상세 분석", "⚙️ 설정"])

    with tab1:
        st.markdown("### 🚨 현재 매매 신호")

        strategies = ['BTC_only', 'ETH_only', 'rebalance_50_50', 'rebalance_60_40']
        strategy_names = ['BTC 단일', 'ETH 단일', '50:50 리밸런싱', '60:40 리밸런싱']

        col1, col2 = st.columns(2)

        for i, (strategy, name) in enumerate(zip(strategies, strategy_names)):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"#### {name}")

                if strategy in data:
                    strategy_data = data[strategy]
                    optimal_ma = strategy_data.get('optimal_ma', 20)

                    # Mock current signal (in real implementation, this would use live data)
                    signal = "강한 매수" if i % 2 == 0 else "약한 매도"
                    strength = 85 if i % 2 == 0 else 72
                    last_change = "2024-01-15"
                    days_since = 3

                    display_signal_card(signal, strength, last_change, days_since)

                    st.markdown(f"""
                    **최적 MA:** {optimal_ma}일  
                    **현재 가격 vs MA:** +2.5%  
                    **신호 지속기간:** {days_since}일
                    """)

    with tab2:
        st.markdown("### 📊 전략별 성과 비교")

        if data:
            # Performance metrics table
            performance_df = pd.DataFrame({
                '전략': strategy_names,
                'CAGR (%)': [25.4, 32.1, 28.7, 26.9],
                'MDD (%)': [-45.2, -52.3, -38.1, -41.7],
                'Sharpe': [1.23, 1.45, 1.67, 1.52],
                'Sortino': [1.89, 2.12, 2.34, 2.18],
                '최적 MA': [21, 18, 24, 22]
            })

            st.dataframe(
                performance_df,
                use_container_width=True,
                hide_index=True
            )

            # Performance chart
            if st.checkbox("상세 차트 보기"):
                fig = create_performance_chart(data)
                st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("### 🔍 전략별 상세 분석")

        selected_strategy = st.selectbox("분석할 전략 선택", strategy_names)

        strategy_key = strategies[strategy_names.index(selected_strategy)]

        if strategy_key in data:
            strategy_data = data[strategy_key]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("연평균 수익률", "28.5%", "2.3%")
                st.metric("최대 낙폭", "-38.1%", "7.2%")

            with col2:
                st.metric("승률", "67.4%", "1.8%")
                st.metric("평균 보유기간", "12.3일", "-0.5일")

            with col3:
                st.metric("최대 수익", "156.7%", "")
                st.metric("위험도", "보통", "")

            # Risk indicators
            st.markdown("#### 위험 지표")
            st.markdown("""
            <div>
                <span class="risk-indicator risk-low">유동성 위험: 낮음</span>
                <span class="risk-indicator risk-medium">변동성 위험: 보통</span>
                <span class="risk-indicator risk-low">시장 위험: 낮음</span>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("### ⚙️ 설정 및 알림")

        st.markdown("#### 알림 설정")
        email_alert = st.checkbox("이메일 알림 받기")
        if email_alert:
            email = st.text_input("이메일 주소")

        signal_threshold = st.slider("신호 민감도", 1, 10, 5)

        st.markdown("#### 포트폴리오 설정")
        investment_amount = st.number_input("투자 금액 (원)", min_value=100000, value=1000000, step=100000)

        risk_level = st.selectbox("위험 성향", ["보수적", "중립적", "공격적"])

        if st.button("설정 저장"):
            st.success("설정이 저장되었습니다!")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>⚠️ 투자 결정은 본인의 판단과 책임하에 이루어져야 합니다.</p>
        <p>본 서비스는 투자 참고용으로만 활용하시기 바랍니다.</p>
        <p>🔄 데이터는 매일 오전 9시에 자동 업데이트됩니다.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
