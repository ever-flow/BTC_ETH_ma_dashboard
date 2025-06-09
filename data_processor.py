import pandas as pd
import numpy as np
import yfinance as yf
import warnings
import datetime
from dateutil.relativedelta import relativedelta
import json
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import time

warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class StrategyResult:
    """Strategy analysis result data class"""
    strategy_name: str
    optimal_ma: int
    cagr: float
    mdd: float
    sharpe_ratio: float
    sortino_ratio: float
    combined_score: float
    win_rate: float
    total_trades: int
    current_signal: str
    signal_strength: float
    last_signal_change: str
    backtest_data: Dict

class CryptoStrategyAnalyzer:
    """Advanced cryptocurrency moving average strategy analyzer"""

    def __init__(self):
        self.data = None
        self.strategies = {
            'BTC_only': 'BTC 단일 투자',
            'ETH_only': 'ETH 단일 투자', 
            'rebalance_50_50': '50:50 리밸런싱',
            'rebalance_60_40': '60:40 리밸런싱'
        }
        self.ma_ranges = {
            'short': range(5, 31),    # 5-30일
            'medium': range(20, 61),  # 20-60일
            'long': range(50, 201)    # 50-200일
        }

    def fetch_crypto_data(self, start_date: str = "2018-01-01") -> pd.DataFrame:
        """Enhanced crypto data fetching with error handling and validation"""
        try:
            logger.info("암호화폐 데이터 수집 시작...")

            # Download data with retry mechanism
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    btc = yf.download("BTC-USD", start=start_date, progress=False)
                    eth = yf.download("ETH-USD", start=start_date, progress=False)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"데이터 수집 시도 {attempt + 1} 실패, 재시도 중...")
                    time.sleep(2)

            # Validate data
            if btc.empty or eth.empty:
                raise ValueError("데이터 수집 실패: 빈 데이터셋")

            # Create aligned DataFrame
            df = pd.DataFrame()
            df['BTC'] = btc['Close']
            df['ETH'] = eth['Close']

            # Remove NaN values and validate
            df = df.dropna()

            if len(df) < 365:  # Need at least 1 year of data
                raise ValueError("충분한 데이터가 없습니다")

            logger.info(f"데이터 수집 완료: {len(df)}개 데이터 포인트")
            return df

        except Exception as e:
            logger.error(f"데이터 수집 오류: {e}")
            raise

    def calculate_enhanced_metrics(self, returns: pd.Series, period_returns: pd.Series = None) -> Dict:
        """Calculate enhanced performance metrics"""
        if returns.empty:
            return {}

        # Remove NaN values
        returns = returns.dropna()

        # Basic metrics
        total_return = (1 + returns).prod() - 1
        num_years = len(returns) / 252  # Trading days per year
        cagr = (1 + total_return) ** (1/num_years) - 1 if num_years > 0 else 0

        # Volatility and Sharpe
        volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = (cagr - 0.02) / volatility if volatility > 0 else 0  # Assuming 2% risk-free rate

        # Sortino ratio (downside deviation)
        downside_returns = returns[returns < 0]
        downside_deviation = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        sortino_ratio = (cagr - 0.02) / downside_deviation if downside_deviation > 0 else 0

        # Maximum Drawdown
        cumulative_returns = (1 + returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdowns = (cumulative_returns - rolling_max) / rolling_max
        max_drawdown = drawdowns.min()

        # Win rate
        win_rate = len(returns[returns > 0]) / len(returns) if len(returns) > 0 else 0

        # Enhanced combined score with time decay weighting
        if period_returns is not None:
            # Time-weighted performance (more weight on recent performance)
            recent_weight = 0.7
            historical_weight = 0.3

            recent_sortino = self._calculate_sortino(period_returns)
            historical_sortino = sortino_ratio

            combined_score = (recent_weight * recent_sortino + 
                            historical_weight * historical_sortino)
        else:
            combined_score = sortino_ratio

        return {
            'cagr': cagr,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'total_return': total_return,
            'combined_score': combined_score,
            'num_trades': len(returns)
        }

    def _calculate_sortino(self, returns: pd.Series) -> float:
        """Calculate Sortino ratio"""
        if returns.empty:
            return 0

        returns = returns.dropna()
        mean_return = returns.mean() * 252
        downside_returns = returns[returns < 0]
        downside_deviation = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0

        return (mean_return - 0.02) / downside_deviation if downside_deviation > 0 else 0

    def backtest_ma_strategy(self, data: pd.DataFrame, ma_period: int, 
                           strategy_type: str = 'BTC_only') -> Dict:
        """Enhanced backtesting with multiple strategy types"""
        try:
            if strategy_type == 'BTC_only':
                price_data = data['BTC'].copy()
            elif strategy_type == 'ETH_only':
                price_data = data['ETH'].copy()
            else:  # Rebalancing strategies
                # For rebalancing, we'll use a portfolio approach
                if strategy_type == 'rebalance_50_50':
                    weights = [0.5, 0.5]
                else:  # rebalance_60_40
                    weights = [0.6, 0.4]

                # Create portfolio returns
                btc_returns = data['BTC'].pct_change()
                eth_returns = data['ETH'].pct_change()

                portfolio_returns = (weights[0] * btc_returns + weights[1] * eth_returns)
                price_data = (1 + portfolio_returns.fillna(0)).cumprod() * 100

            # Calculate moving average
            ma = price_data.rolling(window=ma_period, min_periods=ma_period).mean()

            # Generate signals
            signals = pd.Series(index=price_data.index, dtype=float)
            signals[price_data > ma] = 1  # Buy signal
            signals[price_data <= ma] = 0  # Sell signal (hold cash)
            signals = signals.fillna(method='ffill').fillna(0)

            # Calculate strategy returns
            price_returns = price_data.pct_change()
            strategy_returns = signals.shift(1) * price_returns
            strategy_returns = strategy_returns.dropna()

            # Calculate metrics for different periods
            all_period_metrics = self.calculate_enhanced_metrics(strategy_returns)

            # Recent period metrics (last 2 years for time weighting)
            recent_cutoff = len(strategy_returns) - min(504, len(strategy_returns) // 2)  # ~2 years or half data
            recent_returns = strategy_returns.iloc[recent_cutoff:]
            recent_metrics = self.calculate_enhanced_metrics(recent_returns)

            # Enhanced combined score
            if len(recent_returns) > 0:
                all_period_metrics['combined_score'] = (
                    0.3 * all_period_metrics.get('sortino_ratio', 0) + 
                    0.7 * recent_metrics.get('sortino_ratio', 0)
                )

            # Trading analysis
            position_changes = signals.diff()
            trades = len(position_changes[position_changes != 0])

            # Current signal analysis
            current_price = price_data.iloc[-1]
            current_ma = ma.iloc[-1]
            current_signal = "매수" if current_price > current_ma else "매도"

            # Signal strength based on price-MA divergence
            price_ma_ratio = current_price / current_ma if current_ma > 0 else 1
            if price_ma_ratio > 1.02:
                signal_strength = min(95, 50 + (price_ma_ratio - 1) * 1000)
                current_signal = "강한 매수"
            elif price_ma_ratio > 1:
                signal_strength = 50 + (price_ma_ratio - 1) * 500
                current_signal = "약한 매수"
            elif price_ma_ratio < 0.98:
                signal_strength = min(95, 50 + (1 - price_ma_ratio) * 1000)
                current_signal = "강한 매도"
            else:
                signal_strength = 50 + (1 - price_ma_ratio) * 500
                current_signal = "약한 매도"

            return {
                **all_period_metrics,
                'ma_period': ma_period,
                'total_trades': trades,
                'current_signal': current_signal,
                'signal_strength': min(99, max(1, signal_strength)),
                'current_price_ma_ratio': price_ma_ratio,
                'cumulative_returns': (1 + strategy_returns).cumprod().tolist(),
                'signals': signals.tolist(),
                'recent_performance': recent_metrics
            }

        except Exception as e:
            logger.error(f"백테스팅 오류 ({strategy_type}, MA={ma_period}): {e}")
            return {}

    def find_optimal_ma(self, data: pd.DataFrame, strategy_type: str = 'BTC_only') -> StrategyResult:
        """Find optimal MA period using enhanced scoring"""
        logger.info(f"{strategy_type} 전략 최적화 시작...")

        best_score = -999
        best_ma = 20
        best_result = {}

        # Test different MA periods based on strategy type
        if strategy_type in ['BTC_only', 'ETH_only']:
            test_range = range(5, 101)  # 5-100 days for single asset
        else:
            test_range = range(10, 61)  # 10-60 days for portfolio strategies

        # Parallel processing for faster optimization
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.backtest_ma_strategy, data, ma_period, strategy_type): ma_period
                for ma_period in test_range
            }

            for future in futures:
                try:
                    result = future.result(timeout=30)
                    ma_period = futures[future]

                    if result and 'combined_score' in result:
                        score = result['combined_score']
                        if score > best_score:
                            best_score = score
                            best_ma = ma_period
                            best_result = result

                except Exception as e:
                    logger.warning(f"MA {futures[future]} 최적화 실패: {e}")

        # Create StrategyResult
        strategy_result = StrategyResult(
            strategy_name=self.strategies[strategy_type],
            optimal_ma=best_ma,
            cagr=best_result.get('cagr', 0) * 100,
            mdd=best_result.get('max_drawdown', 0) * 100,
            sharpe_ratio=best_result.get('sharpe_ratio', 0),
            sortino_ratio=best_result.get('sortino_ratio', 0),
            combined_score=best_score,
            win_rate=best_result.get('win_rate', 0) * 100,
            total_trades=best_result.get('total_trades', 0),
            current_signal=best_result.get('current_signal', 'N/A'),
            signal_strength=best_result.get('signal_strength', 50),
            last_signal_change=datetime.datetime.now().strftime('%Y-%m-%d'),
            backtest_data=best_result
        )

        logger.info(f"{strategy_type} 최적화 완료: MA={best_ma}, Score={best_score:.3f}")
        return strategy_result

    def run_full_analysis(self) -> Dict:
        """Run complete analysis for all strategies"""
        logger.info("전체 전략 분석 시작...")

        try:
            # Fetch data
            self.data = self.fetch_crypto_data()

            results = {}

            # Analyze each strategy
            for strategy_type in self.strategies.keys():
                try:
                    strategy_result = self.find_optimal_ma(self.data, strategy_type)
                    results[strategy_type] = {
                        'strategy_name': strategy_result.strategy_name,
                        'optimal_ma': strategy_result.optimal_ma,
                        'cagr': strategy_result.cagr,
                        'mdd': strategy_result.mdd,
                        'sharpe_ratio': strategy_result.sharpe_ratio,
                        'sortino_ratio': strategy_result.sortino_ratio,
                        'combined_score': strategy_result.combined_score,
                        'win_rate': strategy_result.win_rate,
                        'total_trades': strategy_result.total_trades,
                        'current_signal': strategy_result.current_signal,
                        'signal_strength': strategy_result.signal_strength,
                        'last_signal_change': strategy_result.last_signal_change,
                        'backtest_data': strategy_result.backtest_data
                    }
                except Exception as e:
                    logger.error(f"{strategy_type} 분석 실패: {e}")
                    continue

            # Add metadata
            results['metadata'] = {
                'last_update': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_points': len(self.data),
                'analysis_period': f"{self.data.index[0].strftime('%Y-%m-%d')} ~ {self.data.index[-1].strftime('%Y-%m-%d')}",
                'version': '2.0.0'
            }

            logger.info("전체 분석 완료")
            return results

        except Exception as e:
            logger.error(f"전체 분석 실패: {e}")
            return {}

    def save_results(self, results: Dict, filename: str = 'strategy_results.json'):
        """Save analysis results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            logger.info(f"결과 저장 완료: {filename}")
        except Exception as e:
            logger.error(f"결과 저장 실패: {e}")

def main():
    """Main function for standalone execution"""
    analyzer = CryptoStrategyAnalyzer()
    results = analyzer.run_full_analysis()

    if results:
        analyzer.save_results(results)
        print("\n=== 분석 결과 요약 ===")
        for strategy_type, data in results.items():
            if strategy_type != 'metadata':
                print(f"\n{data['strategy_name']}:")
                print(f"  최적 MA: {data['optimal_ma']}일")
                print(f"  CAGR: {data['cagr']:.2f}%")
                print(f"  MDD: {data['mdd']:.2f}%")
                print(f"  현재 신호: {data['current_signal']} ({data['signal_strength']:.1f}%)")
    else:
        print("분석 실패")

if __name__ == "__main__":
    main()
