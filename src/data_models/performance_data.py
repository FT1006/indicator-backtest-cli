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
    Explanation of the Ordering
	•	Overall Performance Metrics: These are usually the first items 
    that stakeholders (and automated reporting systems) look at. They 
    tell you, in broad strokes, whether the strategy was profitable.
	•	Risk-Adjusted Performance Metrics: After raw performance, it’s 
    important to understand whether the returns came with excessive 
    risk. Ratios like Sharpe and Sortino are industry standards for 
    this.
	•	Risk Metrics: Maximum drawdown and volatility provide more 
    details on the risk profile. A strategy with high returns but 
    equally high drawdown might not be acceptable.
	•	Trade Statistics: While useful, these are secondary in many 
    reports. They help diagnose whether the strategy is sustainable 
    or if its performance is based on a few outsized trades.
    """