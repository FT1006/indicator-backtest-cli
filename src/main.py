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
import logging

# Import the backtest engine and strategies
from src.backtesting.backtest_engine import BacktestEngine, TwoMAStrategy, TwoMACDStrategy

def main():
    try:
        # Load configuration (which may include CLI overrides)
        config_loader = CLIConfigLoader()
        config = config_loader.get_config()
        
        # Set up logging based on the configuration
        logger = setup_logger(config)
        logger.info("Logging is initialized.")
        
        # Prompt the user to choose a generator method
        print("Select a price generation method:")
        print("1. Random Walk")
        print("2. Geometric Brownian Motion")
        print("3. Heston Jump Diffusion")
        choice = input("Enter the number (1-3): ").strip()

        if choice == '1':
            generator = RandomWalkGenerator()
        elif choice == '2':
            # Fix: use self.drift rather than a missing _drift in our generator code.
            generator = GeometricBrownianMotionPriceGenerator()
        elif choice == '3':
            generator = HestonJumpDiffusionPriceGenerator()
        else:
            print("Invalid choice. Exiting.")
            sys.exit(1)

        # Create the initial PriceData object.
        # For example, symbol "TEST", starting price 100, and starting time now.
        initial_time = datetime.now()
        # Create an initial PricePoint; here, open, high, low, close are all the same.
        initial_price_point = PricePoint(initial_time, 100, 100, 100, 100, 1000)
        price_data = PriceData("TEST", initial_price_point.close, initial_time)
        price_data.add_price_point(initial_price_point)

        # Generate 582 minutes of data.
        for _ in range(582):
            generator.generate_minute_price(price_data)
        
        # Initialize and run the backtest engine
        engine = BacktestEngine(price_data)
        engine.add_strategy(TwoMAStrategy(price_data, fast_period=10, slow_period=20))
        engine.add_strategy(TwoMACDStrategy(price_data, fast=12, slow=26, signal=9))
        results = engine.run()
        
        # Print out all signals from each strategy
        for strategy_name, result in results.items():
            print(f"\nStrategy: {strategy_name}")
            print("Trade Signals:")
            for signal in result['signals']:
                print(signal)
            print("-----")
        
        # Plot the generated price data
        plot_price_data(price_data)
    except Exception as e:
        logger.error("An error occurred", exc_info=True)
        # Optionally, re-raise the exception if you want the program to terminate
        raise

if __name__ == '__main__':
    main()