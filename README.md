# Indicator Backtest CLI

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line interface for backtesting trading strategies using synthetic price data with various financial models.

## Overview

The Indicator Backtest CLI provides a framework for:
- Generating synthetic price data using different financial models
- Implementing and testing trading strategies based on technical indicators
- Analyzing strategy performance through detailed metrics
- Visualizing price data, indicators, and executed trades

## Features

- **Price Generation Models**:
  - Random Walk
  - Geometric Brownian Motion
  - Heston Jump Diffusion
  
- **Technical Indicators**:
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - MACD (Moving Average Convergence Divergence)

- **Trading Strategies**:
  - Two Moving Averages (2MA)
  - Two MACD (2MACD)
  
- **Key Capabilities**:
  - Strategy performance evaluation
  - Trade execution simulation
  - Interactive CLI interface
  - Configurable logging

## Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/yourusername/indicator-backtest-cli.git
cd indicator-backtest-cli
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run the main script to start the CLI:

```bash
python src/main.py
```

The application will guide you through:

1. Selecting a price generation model
2. Choosing a trading strategy
3. Running the backtest simulation
4. Viewing performance results and metrics

## Project Structure

```
indicator-backtest-cli/
├── src/
│   ├── backtesting/      # Core backtesting engine and performance metrics
│   ├── config/           # Configuration management
│   ├── controllers/      # Application flow controllers
│   ├── data_models/      # Data structures for prices, signals, trades
│   ├── indicators/       # Technical indicator implementations
│   ├── utils/            # Utility functions and visualization
│   ├── main.py           # Application entry point
│   └── price_generators.py # Price simulation models
```

## Extending the Framework

### Adding New Indicators

Extend the `PriceIndicators` class in `src/indicators/price_indicators.py`:

```python
def my_indicator(self, param1=10, param2=20):
    # Implementation...
    return [IndicatorValue(time=t, indicator="MyIndicator", value=val)
            for t, val in zip(times, values)]
```

### Creating New Strategies

Subclass the `Strategy` class in `src/backtesting/backtest_engine.py`:

```python
class MyNewStrategy(Strategy):
    def __init__(self, price_data, param1=10, param2=20):
        super().__init__(price_data)
        self.param1 = param1
        self.param2 = param2
        self.name = "MyStrategy"

    def generate_signals(self):
        # Signal generation logic...
        return signals
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project Status

Active development - beta version