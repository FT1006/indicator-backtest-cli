from typing import List, Dict
from src.data_models.price_data import PriceData
from src.indicators.price_indicators import PriceIndicators
from src.data_models.signal import ordersignal

class Strategy:
    """
    A base class for all trading strategies.

    Attributes:
        price_data (PriceData): The historical price data used for generating signals.
        indicators (PriceIndicators): The price indicators used for generating signals.
    """
    def __init__(self, price_data: PriceData):
        self.price_data = price_data
        self.indicators = PriceIndicators(price_data)
    
    def generate_signals(self) -> List[ordersignal]:
        """
        Generates trading signals based on the strategy.

        Returns:
            List[ordersignal]: A list of ordersignal objects representing the trading signals.
        """
        raise NotImplementedError("Subclasses must implement generate_signals")

class TwoMAStrategy(Strategy):
    """
    A trading strategy based on the crossover of two moving averages.
    """
    def __init__(self, price_data: PriceData, fast_period=10, slow_period=20):
        super().__init__(price_data)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.name = "2MA"
    
    def generate_signals(self) -> List[ordersignal]:
        """
        Generates trading signals based on the crossover of two moving averages.

        This method iterates through the moving average data, checking for bullish and bearish crossovers.
        A bullish crossover occurs when the fast moving average crosses above the slow moving average, indicating a buy signal.
        A bearish crossover occurs when the fast moving average crosses below the slow moving average, indicating a sell signal.

        Returns:
            List[ordersignal]: A list of ordersignal objects representing the trading signals generated.
        """
        signals = []
        
        # Retrieve moving average values, expecting a list of IndicatorValue objects.
        fast_ma = self.indicators.ma(self.fast_period)
        slow_ma = self.indicators.ma(self.slow_period)
        
        prev_fast = None
        prev_slow = None
        
        # Iterate through moving average data to check for crossovers.
        for fast_val_obj, slow_val_obj in zip(fast_ma, slow_ma):
            time = fast_val_obj.time
            fast_val = fast_val_obj.value
            slow_val = slow_val_obj.value
            
            if prev_fast is not None and prev_slow is not None:
                # Check for bullish crossover (fast MA crosses above slow MA).
                if prev_fast <= prev_slow and fast_val > slow_val:
                    signals.append(ordersignal(
                        time=time,
                        action='BUY',
                        price=self.price_data.get_price_at_time(time).close,
                        strategy=self.name
                    ))
                # Check for bearish crossover (fast MA crosses below slow MA).
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
    """
    A trading strategy based on the crossover of MACD and its signal line.
    """
    def __init__(self, price_data: PriceData, fast=12, slow=26, signal=9):
        super().__init__(price_data)
        self.fast = fast
        self.slow = slow
        self.signal = signal
        self.name = "2MACD"

    def generate_signals(self) -> List[ordersignal]:
        """
        Generates trading signals based on the crossover of MACD and its signal line.

        This method iterates through the MACD data, checking for bullish and bearish crossovers.
        A bullish crossover occurs when the MACD line crosses above the signal line, indicating a buy signal.
        A bearish crossover occurs when the MACD line crosses below the signal line, indicating a sell signal.

        Returns:
            List[ordersignal]: A list of ordersignal objects representing the trading signals generated.
        """
        signals = []
        
        # Retrieve MACD values, expecting a list of MACDValue objects.
        macd_data = self.indicators.macd(self.fast, self.slow, self.signal)
        
        prev_dif = None
        prev_dea = None
        
        # Iterate through MACD data to check for crossovers.
        for data in macd_data:
            time = data.time
            dif = data.dif  # MACD line
            dea = data.dea  # Signal line
            
            if prev_dif is not None and prev_dea is not None:
                # Check for bullish crossover (MACD crosses above signal).
                if prev_dif <= prev_dea and dif > dea:
                    signals.append(ordersignal(
                        time=time,
                        action='BUY',
                        price=self.price_data.get_price_at_time(time).close,
                        strategy=self.name
                    ))
                # Check for bearish crossover (MACD crosses below signal).
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
    """
    A class for running backtests on trading strategies.

    Attributes:
        price_data (PriceData): The historical price data used for the backtest.
        initial_capital (float): The initial capital used for the backtest.
        strategies (List[Strategy]): The list of strategies to be tested.
        signals (List[List[ordersignal]]): The list of trading signals generated by each strategy.
    """
    def __init__(self, price_data: PriceData, initial_capital: float = 100000.0):
        self.price_data = price_data
        self.initial_capital = initial_capital
        self.strategies: List[Strategy] = []
        self.signals = []
        
    def add_strategy(self, strategy: Strategy):
        """
        Adds a strategy to the backtest engine.

        Args:
            strategy (Strategy): The strategy to be added.
        """
        self.strategies.append(strategy)
    
    def run(self) -> Dict:
        """
        Runs the backtest for all strategies and returns performance metrics.

        Returns:
            Dict: A dictionary containing the performance metrics of the backtest.
        """
        if not self.strategies:
            print("No strategies to run.")
            return
        
        for strategy in self.strategies:
            self.signals.append(strategy.generate_signals())
