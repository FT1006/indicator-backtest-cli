from src.data_models.trade_record import TradeRecord
from src.data_models.price_data import PriceData
from dataclasses import dataclass
from datetime import datetime
from typing import List
from src.data_models.trade_record import TradeRecord

class TradeManager:
    """
    Manages trades and calculates performance metrics.
    
    Attributes:
        initial_capital: Starting capital for trading
    """
    def __init__(self, initial_capital: float = 100000.0):
        """Initializes TradeManager with starting capital.
        
        Args:
            initial_capital: Starting capital for trading. Defaults to 100000.0.
        """
        self.trades = []
        self.initial_capital = initial_capital
        self.no_of_shares = 0
        self.current_price = 0
        self.cash = initial_capital
        self.current_quantity = 0
        self.capital = self.cash + self.current_price * self.current_quantity
        self.profit = self.capital - initial_capital


    def buy(self, price: float, no_of_shares_traded: float):
        """
        Execute a buy trade.
        
        Args:
            price: Price per share at which to buy
            no_of_shares_traded: Number of shares to purchase
            
        Returns:
            bool: True if order executed successfully, False if insufficient capital
            
        Note:
            Updates cash balance, current position quantity, and capital
            Records trade in trades list
        """
        print("remaining cash before buy: ", self.cash)
        self.current_price = price
        if self.cash >= price * no_of_shares_traded:
            self.cash -= price * no_of_shares_traded
            self.current_quantity += no_of_shares_traded
            self.capital = self.cash + self.current_price * self.current_quantity
            self.trades.append(TradeRecord(
                time=datetime.now(),
                action='BUY',
                price=price,
                traded_shares=no_of_shares_traded,
                available_cash=self.cash,
                capital=self.capital
            ))
            print("remaining cash after buy: ", self.cash, "capital: ", self.capital)
            return True  # Order executed successfully
        return False  # Order not executed due to insufficient capital

    def sell(self, price: float, no_of_shares_traded: float):
        """
        Execute a sell trade.
        
        Args:
            price: Price per share at which to sell
            no_of_shares_traded: Number of shares to sell
            
        Returns:
            bool: True if order executed successfully, False if insufficient shares
            
        Note:
            Updates cash balance, current position quantity, and capital
            Records trade in trades list
        """
        print("remaining cash before sell: ", self.cash)
        self.current_price = price
        if self.current_quantity >= no_of_shares_traded: 
            self.current_quantity -= no_of_shares_traded
            self.cash += price * no_of_shares_traded
            self.capital = self.cash + self.current_price * self.current_quantity
            self.trades.append(TradeRecord(
                time=datetime.now(),
                action='SELL',
                price=price,
                traded_shares=no_of_shares_traded,
                available_cash=self.cash,
                capital=self.capital
            ))
            print("remaining cash after sell: ", self.cash, "capital: ", self.capital)
            return True  # Order executed successfully
        return False  # Order not executed due to insufficient capital
            

    def get_trades(self) -> List[TradeRecord]:
        """
        Get all trades executed so far.
        
        Returns:
            List[TradeRecord]: List of trade records in chronological order
        """
        return self.trades

    def get_trade_count(self) -> int:
        """
        Get the number of trades executed so far.
        
        Returns:
            int: Count of trades in the trade history
        """
        return len(self.trades)