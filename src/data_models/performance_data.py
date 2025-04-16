from dataclasses import dataclass
from typing import Optional

@dataclass
class BacktestResult:
    # 1. Overall Performance Metrics
    initial_capital: float
    final_capital: float
    total_return: float  # Could be in absolute terms or percentage
    annualized_return: float  # Compound annual growth rate (CAGR)
    
    # 2. Risk-Adjusted Performance Metrics
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    calmar_ratio: Optional[float] = None
    
    # 3. Risk Metrics
    max_drawdown: Optional[float] = None
    volatility: Optional[float] = None  # Standard deviation of returns
    
    # 4. Trade Statistics
    total_trades: Optional[int] = None
    win_rate: Optional[float] = None  # As a percentage or decimal fraction
    profit_factor: Optional[float] = None
    average_trade_return: Optional[float] = None

    """
    Represents the results of a backtest, including various performance metrics.

    Attributes:
        initial_capital (float): The initial capital used in the backtest.
        final_capital (float): The final capital after the backtest.
        total_return (float): The total return of the backtest, which could be in absolute terms or as a percentage.
        annualized_return (float): The compound annual growth rate (CAGR) of the backtest.
        sharpe_ratio (Optional[float]): The Sharpe ratio of the backtest, a measure of risk-adjusted return. Defaults to None.
        sortino_ratio (Optional[float]): The Sortino ratio of the backtest, a measure of risk-adjusted return. Defaults to None.
        calmar_ratio (Optional[float]): The Calmar ratio of the backtest, a measure of risk-adjusted return. Defaults to None.
        max_drawdown (Optional[float]): The maximum drawdown of the backtest, a measure of risk. Defaults to None.
        volatility (Optional[float]): The volatility of the backtest, measured as the standard deviation of returns. Defaults to None.
        total_trades (Optional[int]): The total number of trades executed during the backtest. Defaults to None.
        win_rate (Optional[float]): The win rate of the backtest, as a percentage or decimal fraction. Defaults to None.
        profit_factor (Optional[float]): The profit factor of the backtest, a measure of the strategy's profitability. Defaults to None.
        average_trade_return (Optional[float]): The average return per trade of the backtest. Defaults to None.
    """