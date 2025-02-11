# indicator-backtest-cli
# indicator-backtest-cli

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line interface for financial instrument backtesting with multiple price generation models and trading strategies.

## Overview

The indicator-backtest-cli is a sophisticated backtesting environment that enables users to:

- Generate synthetic price data using different financial models
- Test trading strategies against historical/simulated market data
- Analyze strategy performance through detailed metrics and visualizations

## Features

- **Price Generation Models**:
  - Random Walk
  - Geometric Brownian Motion
  - Heston Jump Diffusion
  
- **Trading Strategies**:
  - Two Moving Averages (2MA)
  - Two MACD (2MACD)
  
- **Key Capabilities**:
  - Performance metrics calculation
  - Trade execution simulation
  - Interactive CLI interface
  - Configurable logging

## Installation
bash
git clone https://github.com/yourusername/indicator-backtest-cli.git
cd indicator-backtest-cli
pip install -e .

## Usage
bash
python src/main.py

Example workflow:
1. Select price generation model (1-3)
2. Choose trading strategy (1-3)
3. Review generated price data
4. Analyze backtest results
5. View performance metrics

## Configuration

The application can be configured through:
- `config/cli_config.yaml` for default parameters
- Environment variables
- Runtime CLI inputs

Key configurable parameters:
- Logging verbosity
- Simulation duration
- Strategy parameters
- Price generation settings

## Contributing

Contributions are welcome! Please follow these steps:
1. Open an issue to discuss proposed changes
2. Fork the repository
3. Create a feature branch
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Status

Active development - v0.1.0 (Beta)