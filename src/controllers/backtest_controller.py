from src.backtesting.backtest_engine import BacktestEngine, TwoMAStrategy, TwoMACDStrategy
from src.backtesting.trade import TradeManager
from src.data_models.price_data import PriceData
from src.price_generators import (
    RandomWalkGenerator,
    GeometricBrownianMotionPriceGenerator,
    HestonJumpDiffusionPriceGenerator
)
from datetime import datetime, timedelta

class BacktestController:
    def __init__(self):
        self.trade_manager = TradeManager()
        self.engine = BacktestEngine(self.trade_manager)

    def allin(self, engine: BacktestEngine):
        """
        Run a backtest for selected strategies. Buy and sell all in.
        """

        self.engine.run()
        # Trade all signals in the backtest
        for signal in self.engine.signals:
            if signal.ordersignal.action == 'BUY':
                self.trade_manager.buy(signal.price, self.trade_manager.capital/signal.price)
            elif signal.ordersignal.action == 'SELL':
                self.trade_manager.sell(signal.price, self.trade_manager.current_quantity)
