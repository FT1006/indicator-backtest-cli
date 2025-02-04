import random
import math
from datetime import timedelta, datetime
from data_models.price_data import PriceData, PricePoint
from abc import ABC, abstractmethod

class PriceBaseGenerator(ABC):
    """
    Abstract base class to enforce the generation of minute-level pricing.
    Each subclass must implement generate_minute_price, which updates the 
    StockData object with a new price point.
    """
    @abstractmethod
    def generate_minute_price(self, stock_data, time):
        pass

class RandomWalkGenerator(PriceBaseGenerator):
    def __init__(self, volatility, drift):
        self._volatility = volatility
        self._drift = drift
        self._last_price = None
    
    def generate_minute_price(self, stock_data: PriceData, time):
        if self._last_price is None:
            self._last_price = stock_data.get_latest_price()

        fluctuation = random.uniform(-self._volatility, self._volatility)
        drft = random.uniform(-self._drift, self._drift)
        if stock_data.get_price_points_count() == 0 or stock_data.get_price_points_count() % 390 == 0: # Every 390 minutes (1 trading day)
            new_price = self._last_price.close + fluctuation + drft
        else:
            new_price = self._last_price.close + fluctuation
        
        # Create minimal open/high/low/close data
        open_price = self._last_price.close
        close_price = new_price
        high_price = max(open_price, close_price) + random.uniform(0, self._volatility)
        low_price = min(open_price, close_price) - random.uniform(0, self._volatility)
        volume = random.randint(100, 1000)

        # Update the StockData object with the new price point
        stock_data.add_price_point(PricePoint(time, open_price, high_price, low_price, close_price, volume))
        self._last_price = stock_data.get_latest_price()
        volume = random.randint(100, 1000)