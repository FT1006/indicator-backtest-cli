project-root/
├── README.md
├── architecture.md    # Documentation on design and architecture
├── src/
│   ├── main.py            # Entry point of the application
│   ├── price_generators.py  # Price data generator modules
│   ├── controllers/
│   │   └── backtest_controller.py  # Orchestrates the backtesting workflow
│   │   └── cli.py             # CLI interface for user input/output
│   ├── indicators/        # Indicator calculation modules
│   │   ├── base.py  # Interface/abstract class for indicators
│   │   ├── price_indicators.py  # Price indicators (MACD, RSI, etc.)
│   ├── backtesting/       # Core backtesting logic
│   │   ├── backtesting_engine.py  # Detects signals and drives simulation
│   │   ├── trade.py     # Executes trades and logs trade data
│   │   └── performance_calculator.py  # Computes performance metrics
│   ├── utils/             # Utility modules (data aggregation, plotting, etc.)
│   │   ├── data_aggregator.py     # Aggregates raw price data into timeframes
│   │   └── chart_plotting.py      # Plots charts of price chart, indicator values and trades
│   └── models/            # Data models representing domain entities
│       ├── price_data.py   # Price data point structure
│       ├── trade.py        # Trade record structure
│       └── indicator_value.py  # Indicator value structure
└── tests/                 # Unit and integration tests
