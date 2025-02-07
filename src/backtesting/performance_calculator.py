import math
import statistics
from typing import List
from src.data_models.performance_data import BacktestResult

class BacktestPerformance:
    def __init__(self, risk_free_rate: float = 0.0, periods_per_year: int = 252):
        """
        :param risk_free_rate: Annual risk-free rate (e.g., 0.02 for 2%)
        :param periods_per_year: Number of trading periods per year (default is 252 for daily data)
        """
        self.risk_free_rate = risk_free_rate
        self.periods_per_year = periods_per_year

    def calculate(self, equity_curve: List[float], trades: List[float]) -> BacktestResult:
        """
        Calculate performance metrics based on the provided equity curve and list of trade returns.
        
        :param equity_curve: List of portfolio equity values in chronological order.
        :param trades: List of individual trade returns (can be absolute numbers or percentages).
        :return: BacktestResult containing multiple performance and risk metrics.
        """
        if not equity_curve:
            raise ValueError("Equity curve cannot be empty")

        # 1. Overall Performance Metrics
        initial_capital = equity_curve[0]
        final_capital = equity_curve[-1]
        total_return = (final_capital - initial_capital) / initial_capital

        # Calculate the duration in years based on the number of periods (assumes daily periods)
        num_periods = len(equity_curve) - 1
        years = num_periods / self.periods_per_year if num_periods > 0 else 0
        annualized_return = (
            (final_capital / initial_capital) ** (1 / years) - 1
            if years > 0
            else 0.0
        )

        # 2. Risk-Adjusted Performance Metrics & Risk Metrics using daily returns
        daily_returns = []
        if len(equity_curve) >= 2:
            for i in range(1, len(equity_curve)):
                previous = equity_curve[i - 1]
                # Prevent division by zero (though unlikely in typical backtest equity curves)
                daily_return = ((equity_curve[i] - previous) / previous) if previous != 0 else 0.0
                daily_returns.append(daily_return)

        # Volatility: annualized standard deviation of daily returns
        if len(daily_returns) > 1:
            daily_std = statistics.stdev(daily_returns)
            volatility = daily_std * math.sqrt(self.periods_per_year)
        else:
            volatility = None

        # Sharpe Ratio: using the risk-free rate adjusted to a daily rate
        if len(daily_returns) > 1 and volatility not in (None, 0):
            risk_free_daily = self.risk_free_rate / self.periods_per_year
            excess_return = statistics.mean(daily_returns) - risk_free_daily
            sharpe_ratio = excess_return / daily_std * math.sqrt(self.periods_per_year)
        else:
            sharpe_ratio = None

        # Sortino Ratio: only considering deviations below the risk-free rate.
        if len(daily_returns) > 1:
            risk_free_daily = self.risk_free_rate / self.periods_per_year
            downside_returns = [r - risk_free_daily for r in daily_returns if r < risk_free_daily]
            if downside_returns:
                downside_std = statistics.stdev(downside_returns)
                sortino_ratio = (statistics.mean(daily_returns) - risk_free_daily) / downside_std * math.sqrt(self.periods_per_year) if downside_std > 0 else None
            else:
                sortino_ratio = None
        else:
            sortino_ratio = None

        # Maximum Drawdown: maximum drop from a peak over the equity curve
        running_max = equity_curve[0]
        max_drawdown = 0.0
        for value in equity_curve:
            if value > running_max:
                running_max = value
            drawdown = (running_max - value) / running_max
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        # Calmar Ratio: annualized return divided by max drawdown (if applicable)
        calmar_ratio = (annualized_return / max_drawdown) if max_drawdown > 0 else None

        # 3. Trade Statistics Calculation
        total_trades = len(trades)
        if total_trades > 0:
            wins = [trade for trade in trades if trade > 0]
            win_rate = len(wins) / total_trades

            gross_profit = sum(trade for trade in trades if trade > 0)
            gross_loss = abs(sum(trade for trade in trades if trade < 0))
            profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else None

            average_trade_return = statistics.mean(trades)
        else:
            win_rate = None
            profit_factor = None
            average_trade_return = None

        # Construct BacktestResult dataclass instance with all the computed metrics.
        return BacktestResult(
            initial_capital=initial_capital,
            final_capital=final_capital,
            total_return=total_return,
            annualized_return=annualized_return,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            max_drawdown=max_drawdown,
            volatility=volatility,
            total_trades=total_trades if total_trades > 0 else None,
            win_rate=win_rate,
            profit_factor=profit_factor,
            average_trade_return=average_trade_return,
        )



