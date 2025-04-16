# Indicator Backtest CLI Exploration Guide

## 1. Repository Structure Overview

```
indicator-backtest-cli/
├── README.md                # Project overview and usage instructions
├── architecture.md         # High-level architecture documentation
├── implementation_flow.md  # Implementation order and notes
├── src/                    # Source code directory
│   ├── backtesting/        # Core backtesting components
│   ├── config/             # Configuration management
│   ├── controllers/        # Application controllers
│   ├── data_models/        # Data structures
│   ├── indicators/         # Trading indicators implementation
│   ├── utils/              # Utility functions
│   ├── main.py             # Application entry point
│   └── price_generators.py # Price data generation models
└── venv/                   # Virtual environment (not part of codebase)
```

### Key Directories and Their Purposes:

- **src/backtesting/**: Contains the core backtesting engine and performance calculation logic
- **src/indicators/**: Implements technical indicators used in trading strategies
- **src/controllers/**: Manages application flow and user interaction
- **src/data_models/**: Defines data structures for price data, trades, and signals
- **src/utils/**: Provides support functionality like logging and data visualization

## 2. Core Components and Their Functions

### Price Generation
- **Price Generators** (`src/price_generators.py`): Creates synthetic price data using different financial models:
  - Random Walk
  - Geometric Brownian Motion
  - Heston Jump Diffusion

### Indicators
- **Base Indicator** (`src/indicators/base.py`): Abstract base class for indicators
- **Price Indicators** (`src/indicators/price_indicators.py`): Concrete implementations like SMA, EMA, MACD

### Strategies
- **Strategy** (in `src/backtesting/backtest_engine.py`): Base class for all trading strategies
- **Implementation Strategies**:
  - TwoMAStrategy: Uses two moving average crossovers
  - TwoMACDStrategy: Uses MACD indicator signals

### Backtesting
- **Backtest Engine** (`src/backtesting/backtest_engine.py`): Executes strategies and generates signals
- **Trade Manager** (`src/backtesting/trade.py`): Handles trade execution and tracking
- **Performance Calculator** (`src/backtesting/performance_calculator.py`): Computes performance metrics

### Controllers
- **Backtest Controller** (`src/controllers/backtest_controller.py`): Orchestrates the backtesting process
- **CLI Controller** (`src/controllers/cli.py`): Manages user interaction through the command line

## 3. Main Architectural Patterns

### Model-View-Controller (MVC)
- **Models**: Data structures in `data_models/`
- **Views**: CLI interface in `controllers/cli.py` and chart plotting in `utils/chart_plotting.py`
- **Controllers**: Application flow management in `controllers/`

### Strategy Pattern
- Base `Strategy` class with specific implementations (TwoMAStrategy, TwoMACDStrategy)
- Enables easy addition of new strategies without modifying core engine

### Pipeline Architecture
- Clear flow from price generation → indicator calculation → signal generation → trade execution → performance analysis

## 4. Key Implementation Files

1. **src/main.py**: Entry point with step-by-step orchestration of the entire workflow
2. **src/backtesting/backtest_engine.py**: Core engine with strategy implementations
3. **src/indicators/price_indicators.py**: Technical indicator calculations
4. **src/controllers/backtest_controller.py**: Business logic for backtesting
5. **src/data_models/price_data.py**: Fundamental price data structures
6. **src/data_models/signal.py**: Trading signal representation

## 5. Data and Control Flow

1. **Price Data Generation**:
   - User selects a price generation model
   - System generates synthetic price data

2. **Strategy Selection and Signal Generation**:
   - User selects trading strategies
   - System calculates technical indicators
   - Strategies generate buy/sell signals based on indicators

3. **Trade Execution**:
   - BacktestEngine detects signals
   - TradeManager executes trades and tracks positions

4. **Performance Analysis**:
   - PerformanceCalculator computes metrics
   - Results are displayed to the user

## 6. Typical Usage Patterns

### Basic Backtest
```python
# Generate price data
generator = RandomWalkGenerator()
price_data = PriceData("SYMBOL", initial_price=100.0, start_time=datetime.now())
for _ in range(1000):
    generator.generate_minute_price(price_data)

# Create and configure backtest engine
engine = BacktestEngine(price_data)
engine.add_strategy(TwoMAStrategy(price_data, fast_period=10, slow_period=20))

# Execute backtest and analyze results
controller = BacktestController()
controller.allin(engine)
results = controller.get_result()
performance = controller.get_performance()
```

### Custom Strategy Implementation
```python
class MyCustomStrategy(Strategy):
    def __init__(self, price_data):
        super().__init__(price_data)
        self.name = "Custom"
    
    def generate_signals(self):
        signals = []
        # Custom signal generation logic
        return signals
```

## 7. Exploration Strategy

### Where to Start
1. **First Steps**:
   - Review `README.md` and `architecture.md` for high-level understanding
   - Examine `src/main.py` to understand the overall workflow
   - Run the application with `python src/main.py` to see it in action

2. **Intermediate Exploration**:
   - Examine `src/backtesting/backtest_engine.py` to understand strategy implementation
   - Look at `src/indicators/price_indicators.py` to see how technical indicators are calculated
   - Study `src/data_models/` to understand data structures

3. **Advanced Understanding**:
   - Explore `src/backtesting/performance_calculator.py` for performance metrics
   - Review `src/controllers/backtest_controller.py` for orchestration logic
   - Examine `src/price_generators.py` for price simulation models

### Learning Progression
1. **Basic Understanding**: Price data generation → Indicator calculation
2. **Intermediate Understanding**: Strategy implementation → Signal generation
3. **Advanced Understanding**: Trade execution → Performance calculation

## Summary

The Indicator Backtest CLI is a well-structured application for backtesting trading strategies using various price generation models and technical indicators. The architecture follows clean design patterns, making it extensible for new strategies and indicators. By following the exploration strategy outlined above, you can gain a comprehensive understanding of both the high-level architecture and the implementation details.