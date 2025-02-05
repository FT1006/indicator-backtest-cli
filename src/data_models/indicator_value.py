from datetime import datetime
from dataclasses import dataclass

@dataclass
class IndicatorValue:
    """
    Represents a single indicator value at a given time.

    Attributes:
        time (datetime): The timestamp for the indicator value.
        indicator (str): The name of the indicator (e.g., 'SMA', 'EMA').
        value (float): The computed indicator value.
    """
    time: datetime
    indicator: str
    value: float


@dataclass
class MACDValue:
    """
    Represents the MACD indicator values at a given time.

    Attributes:
        time (datetime): The timestamp for the MACD calculation.
        dif (float): The difference between fast EMA and slow EMA.
        dea (float): The exponential moving average of DIF.
        macd (float): The MACD histogram value, computed as 2 * (DIF - DEA).
    """
    time: datetime
    dif: float
    dea: float
    macd: float
