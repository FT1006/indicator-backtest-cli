from dataclasses import dataclass
from datetime import datetime

@dataclass
class TradeRecord:
    """
    Represents a single trade execution record in the backtest.

    Attributes:
        time (datetime): The time the trade was executed.
        action (str): The trade action ('BUY' or 'SELL').
        price (float): The execution price.
        position (float): The resulting number of shares involved in the trade.
        capital (float): The account capital after the trade.
    """
    time: datetime
    action: str
    price: float
    traded_shares: float
    available_cash: float
    capital: float
