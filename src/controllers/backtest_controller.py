from src.backtesting.backtest_engine import BacktestEngine, TwoMAStrategy, TwoMACDStrategy
from src.backtesting.trade import TradeManager
from src.price_generators import (
    RandomWalkGenerator,
    GeometricBrownianMotionPriceGenerator,
    HestonJumpDiffusionPriceGenerator
)
from datetime import datetime, timedelta
from src.backtesting.performance_calculator import BacktestPerformance
import random

class BacktestController:
    def __init__(self):
        self.trade_manager = TradeManager()
        self.engine = None

    def allin(self, engine: BacktestEngine):
        """
        Run a backtest for selected strategies. Buy and sell all in.
        """
        self.engine = engine
        self.engine.run()
        print("check")
        # Trade all signals in the backtest
        for signals in self.engine.signals:
            for signal in signals:
                # signal is already an ordersignal object; use its attributes directly.
                if signal.action == 'BUY':
                    buy_success = self.trade_manager.buy(signal.price, self.trade_manager.cash / signal.price)
                    if buy_success:
                        print(f"BUY: {signal}, remaining cash: {self.trade_manager.cash}")
                    else:
                        print(f"Void Buy: {signal}, remaining cash: {self.trade_manager.cash}")
                elif signal.action == 'SELL':
                    sell_success = self.trade_manager.sell(signal.price, self.trade_manager.current_quantity)
                    if sell_success:
                        print(f"SELL: {signal}")
                    else:
                        print(f"Void Sell: {signal}")

    def fix_pos_limit_exp(self, engine: BacktestEngine, fix_pos_limit_percentage: float = 1.0, max_exposure: float = 1.0):
        """
        Run a backtest for selected strategies with max exposure and fix position limit.
        """
        self.engine = engine
        self.engine.run()
        # Trade all signals in the backtest
        fix_pos_limit_capital = self.trade_manager.initial_capital * fix_pos_limit_percentage
        max_exposure_capital = self.trade_manager.initial_capital * max_exposure
        buy_orders = []
        for signals in self.engine.signals:
            for signal in signals:
                if signal.action == 'BUY' and (self.trade_manager.initial_capital - self.trade_manager.cash > max_exposure_capital):
                    buy_success = self.trade_manager.buy(signal.price, fix_pos_limit_capital / signal.price)
                    if buy_success:                    
                        # Assuming trade_manager.trades holds the recent trade, as a replacement for positions
                        buy_orders.append(self.trade_manager.trades[-1])
                elif signal.action == 'SELL':
                    if buy_orders:
                        self.trade_manager.sell(signal.price, buy_orders.pop(-1).position)

    def get_result(self):
        """
        Get the results of the backtest.
        Returns a dictionary mapping strategy names to a dictionary containing their trade signals.
        """
        if self.trade_manager.get_trade_count() > 0:
            # If the engine holds strategies and signals, group the signals by strategy.
            if self.engine and hasattr(self.engine, "strategies") and len(self.engine.signals) == len(self.engine.strategies):
                results_by_strategy = {}
                for strategy, signals in zip(self.engine.strategies, self.engine.signals):
                    # Use a 'name' attribute if available, otherwise default to the class name.
                    strategy_name = getattr(strategy, "name", strategy.__class__.__name__)
                    results_by_strategy[strategy_name] = {"signals": signals}
                return results_by_strategy
            else:
                # Fallback: return all trades under a generic key.
                return {"All Trades": {"signals": self.trade_manager.get_trades()}}
        else:
            raise ValueError("No trades executed.")
    
    def get_updated_equity_curve(self):
        """
        Get the updated equity curve based on the trades executed.
        """
        equity_curve = [self.trade_manager.initial_capital]
        for trade in self.trade_manager.get_trades():
            equity_curve.append(trade.capital)
        return equity_curve

    def get_performance(self):
        """
        Calculate and print the backtest performance using the updated equity curve and trade returns.
        
        Equity curve is obtained from the trade manager's executed trades.
        Trade returns are computed as the percentage change in equity from one trade to the next.
        """
        # Get the equity curve, which starts with initial capital and then each trade's updated capital
        equity_curve = self.get_updated_equity_curve()
        
        # Compute trade returns based on the change in equity after each trade.
        # (e.g., if equity moves from 100,000 to 102,000, the trade return is 0.02)
        trade_returns = []
        for i in range(1, len(equity_curve)):
            previous = equity_curve[i - 1]
            current = equity_curve[i]
            # Prevent division by zero (though unlikely with a nonzero initial capital)
            trade_return = (current - previous) / previous if previous != 0 else 0.0
            trade_returns.append(trade_return)
        
        # 2% annual risk-free rate is used here
        calc = BacktestPerformance(risk_free_rate=0.02)
        performance_result = calc.calculate(equity_curve, trade_returns)
        
        print(performance_result)