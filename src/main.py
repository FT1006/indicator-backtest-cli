# test_chart_plotting.py
import sys
from datetime import datetime, timedelta
from src.data_models.price_data import PriceData, PricePoint
from src.price_generators import (
    RandomWalkGenerator,
    GeometricBrownianMotionPriceGenerator,
    HestonJumpDiffusionPriceGenerator
)
from src.utils.chart_plotting import plot_price_data
from src.config.cli_config_loader import CLIConfigLoader
from src.utils.log import setup_logger
from src.controllers.backtest_controller import BacktestController
from src.backtesting.performance_calculator import BacktestPerformance
import logging

# Import the backtest engine and strategies
from src.backtesting.backtest_engine import BacktestEngine, TwoMAStrategy, TwoMACDStrategy

def get_generator_choice():
    print("\nSelect a price generation method:")
    print("1. Random Walk")
    print("2. Geometric Brownian Motion")
    print("3. Heston Jump Diffusion")
    while True:
        choice = input("Enter the number (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")

def get_strategy_choice():
    print("\nSelect a trading strategy:")
    print("1. Two Moving Averages (2MA)")
    print("2. Two MACD (2MACD)")
    print("3. Both strategies")
    while True:
        choice = input("Enter the number (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")

def main():
    """Main entry point for the backtesting CLI application.
    
    Orchestrates the complete workflow including:
    - Configuration loading and logging setup
    - User input collection for price generation and strategy selection
    - Price data generation using selected methodology
    - Backtest engine initialization and strategy configuration
    - Backtest execution and performance reporting
    - Results visualization

    The workflow progresses through 11 distinct steps as shown in the console output,
    handling both successful execution paths and error conditions.

    Args:
        None
        
    Returns:
        None
        
    Raises:
        Exception: Propagates any exceptions that occur during execution, after logging
    """
    try:
        print("Step 1: Load CLI configuration and initialize logging.")
        config_loader = CLIConfigLoader()
        config = config_loader.get_config()
        logger = setup_logger(config)
        logger.info("Logging is initialized.")
        print("Step 1 completed: Configuration loaded and logging is set up.")

        print("Step 2: Prompting user for price generator selection.")
        generator_choice = get_generator_choice()
        print(f"Step 2 completed: Selected generator choice: {generator_choice}")

        print("Step 3: Prompting user for trading strategy selection.")
        strategy_choice = get_strategy_choice()
        print(f"Step 3 completed: Selected strategy choice: {strategy_choice}")

        print("Step 4: Initializing price generator based on user choice.")
        if generator_choice == '1':
            generator = RandomWalkGenerator()
        elif generator_choice == '2':
            generator = GeometricBrownianMotionPriceGenerator()
        else:
            generator = HestonJumpDiffusionPriceGenerator()
        print("Step 4 completed: Price generator initialized.")

        print("Step 5: Creating initial price data.")
        initial_time = datetime.now()
        initial_price_point = PricePoint(initial_time, 100, 100, 100, 100, 1000)
        price_data = PriceData("TEST", initial_price_point.close, initial_time)
        price_data.add_price_point(initial_price_point)
        print("Step 5 completed: Initial price data created.")

        print("Step 6: Generating price data for 3 trading days (390 minutes per day).")
        total_minutes = 390 * 3
        logger.info(f"Generating {total_minutes} minutes of price data...")
        for i in range(total_minutes):
            generator.generate_minute_price(price_data)
            # Print a message at the end of each trading day
            if (i + 1) % 390 == 0:
                day = (i + 1) // 390
                print(f"  - Generated data for Day {day}")
        print("Step 6 completed: Price data generation complete.")

        engine = BacktestEngine(price_data)
        print("Step 7: Adding strategies to the engine based on selection.")
        if strategy_choice in ['1', '3']:
            engine.add_strategy(TwoMAStrategy(price_data, fast_period=10, slow_period=20))
        if strategy_choice in ['2', '3']:
            engine.add_strategy(TwoMACDStrategy(price_data, fast=12, slow=26, signal=9))
        print("Step 7 completed: Strategies added.")

        print("Step 8: Initializing backtest engine.")

        backtest_controller = BacktestController()
        backtest_controller.allin(engine)
        print("Step 8 completed: Backtest engine initialized.")

        print("Step 9: Running backtest simulation...")
        results = backtest_controller.get_result()
        print("Step 9 completed: Backtest simulation complete.")

        print("Step 10: Displaying performance results:")
        print("\n=== 3-Day Performance Results ===")
        if not results:
            print("No executed trades were generated by the selected strategies with the current simulation.")
            print("Consider trying a different strategy or adjusting the simulation parameters.")
        else:
            for strategy_name, result in results.items():
                print(f"\nStrategy: {strategy_name}")
                # Use trades from the results instead of the raw signals.
                if 'trades' in result and result['trades']:
                    print("Executed Trades:")
                    for trade in result['trades']:
                        print(f"  Entry Time: {trade.entry_time}, Entry Price: {trade.entry_price:.2f}, "
                              f"Exit Time: {trade.exit_time}, Exit Price: {trade.exit_price:.2f}, "
                              f"Profit: {trade.profit:.2f}")
                    executed_trades = result['trades']
                    total_trades = len(executed_trades)
                    profitable_trades = sum(1 for t in executed_trades if t.profit > 0)
                    losing_trades = sum(1 for t in executed_trades if t.profit <= 0)
                    print(f"\n  Total Trades: {total_trades}")
                    print(f"  Profitable Trades: {profitable_trades}")
                    print(f"  Losing Trades: {losing_trades}")
                else:
                    print("No executed trades for this strategy.")
                print("-----")
        print("Step 10 completed: Performance results displayed.")

        print("Step 11: Calculating performance metrics...")
        performance = backtest_controller.get_performance()
        print(performance)
        print("Step 11 completed: Performance metrics calculated.")
        """
        print("Step 11: Plotting price data and trade signals...")
        logger.info("Plotting price data and signals...")
        plot_price_data(price_data)
        print("Step 11 completed: Price data plotted.")
        """
    except Exception as e:
        logger.error("An error occurred", exc_info=True)
        raise
        
if __name__ == '__main__':
    main()