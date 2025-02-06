from src.data_models.trade_record import TradeRecord
from src.data_models.price_data import PriceData
from src.backtesting.backtest_engine import TradeSignal
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Trade:
    """
    Represents a single trade execution record in the backtest.

    Attributes:
        time (datetime): The time the trade was executed.
        action (str): The trade action ('BUY' or 'SELL').
        price (float): The execution price.
        position (float): The resulting position size.
        capital (float): The account capital after the trade.
    """
    time: datetime
    action: str
    price: float
    position: float
    capital: float

class TradeManager:
    """
    Manages trades and calculates performance metrics.
    """
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.trades = []
        self.capital = initial_capital


    def buy(self, price: float, position: float):
        """
        Execute a buy trade.
        """
        if self.capital > price * position:
            self.capital -= price * position
            self.trades.append(Trade(
                time=datetime.now(),
                action='BUY',
                price=price,
                position=position,
                capital=self.capital
            ))
        else:
            pass

    def sell(self, price: float, position: float):
        """
        Execute a sell trade.
        """
        if 
        self.capital += price * position
        self.trades.append(Trade(
            time=datetime.now(),
            action='SELL',
            price=price,
            position=position,
            capital=self.capital
        ))

    def get_trades(self) -> List[Trade]:
        """
        Get all trades executed so far.
        """
        return self.trades

    def get_trade_count(self) -> int:
        """
        Get the number of trades executed so far.
        """
        return len(self.trades)