from typing import List, Dict
from datetime import datetime
from src.data_models.price_data import PriceData
from src.indicators.price_indicators import PriceIndicators
from src.data_models.signal import ordersignal

class Strategy:
    def __init__(self, price_data: PriceData):
        self.price_data = price_data
        self.indicators = PriceIndicators(price_data)
    
    def generate_signals(self) -> List[ordersignal]:
        raise NotImplementedError("Subclasses must implement generate_signals")

class TwoMAStrategy(Strategy):
    def __init__(self, price_data: PriceData, fast_period=10, slow_period=20):
        super().__init__(price_data)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.name = "2MA"
    
    def generate_signals(self) -> List[ordersignal]:
        signals = []
        
        # Get MA values (each element is an IndicatorValue)
        fast_ma = self.indicators.ma(self.fast_period)
        slow_ma = self.indicators.ma(self.slow_period)
        
        prev_fast = None
        prev_slow = None
        
        # Check for crossovers using attribute access
        for fast_val_obj, slow_val_obj in zip(fast_ma, slow_ma):
            time = fast_val_obj.time
            fast_val = fast_val_obj.value
            slow_val = slow_val_obj.value
            
            if prev_fast is not None and prev_slow is not None:
                # Bullish crossover (fast MA crosses above slow MA)
                if prev_fast <= prev_slow and fast_val > slow_val:
                    signals.append(ordersignal(
                        time=time,
                        action='BUY',
                        price=self.price_data.get_price_at_time(time).close,
                        strategy=self.name
                    ))
                # Bearish crossover (fast MA crosses below slow MA)
                elif prev_fast >= prev_slow and fast_val < slow_val:
                    signals.append(ordersignal(
                        time=time,
                        action='SELL',
                        price=self.price_data.get_price_at_time(time).close,
                        strategy=self.name
                    ))
            
            prev_fast = fast_val
            prev_slow = slow_val
        
        return signals

class TwoMACDStrategy(Strategy):
    def __init__(self, price_data: PriceData, fast=12, slow=26, signal=9):
        super().__init__(price_data)
        self.fast = fast
        self.slow = slow
        self.signal = signal
        self.name = "2MACD"

    def generate_signals(self) -> List[ordersignal]:
        signals = []
        
        # Get MACD values: expecting a list of MACDValue objects.
        macd_data = self.indicators.macd(self.fast, self.slow, self.signal)
        
        prev_dif = None
        prev_dea = None
        
        # Check for crossovers using attribute access on MACDValue objects.
        for data in macd_data:
            time = data.time
            dif = data.dif  # MACD line
            dea = data.dea  # Signal line
            
            if prev_dif is not None and prev_dea is not None:
                # Bullish crossover (MACD crosses above signal)
                if prev_dif <= prev_dea and dif > dea:
                    signals.append(ordersignal(
                        time=time,
                        action='BUY',
                        price=self.price_data.get_price_at_time(time).close,
                        strategy=self.name
                    ))
                # Bearish crossover (MACD crosses below signal)
                elif prev_dif >= prev_dea and dif < dea:
                    signals.append(ordersignal(
                        time=time,
                        action='SELL',
                        price=self.price_data.get_price_at_time(time).close,
                        strategy=self.name
                    ))
            
            prev_dif = dif
            prev_dea = dea
        
        return signals

class BacktestEngine:
    def __init__(self, price_data: PriceData, initial_capital: float = 100000.0):
        self.price_data = price_data
        self.initial_capital = initial_capital
        self.strategies: List[Strategy] = []
        self.signals = []
        
    def add_strategy(self, strategy: Strategy):
        self.strategies.append(strategy)
    
    def run(self) -> Dict:
        """
        Run backtest for all strategies and return performance metrics
        """
        results = {}
        if not self.strategies:
            print("No strategies to run.")
            return
        
        for strategy in self.strategies:
            self.signals.append(strategy.generate_signals())
        
