from src.indicators.base import BaseIndicator
from src.data_models.indicator_value import IndicatorValue, MACDValue

class PriceIndicators(BaseIndicator):
    """
    A class for calculating various price indicators from historical data.

    Attributes:
        close (list): A list of closing prices.
        times (list): A list of corresponding times for the closing prices.
    """

    def ma(self, n=10):
        """
        Calculates the Simple Moving Average (SMA) of the close prices.

        Args:
            n (int, optional): The number of periods to use for the moving average. Defaults to 10.

        Returns:
            list: A list of IndicatorValue objects containing the SMA values aligned with their corresponding times.
        """
        # Simple Moving Average of the close prices.
        ma_values = self.rolling_mean(self.close, n)
        # Align times with computed ma_values -- assuming rolling_mean returns len(close)-n values:
        return [
            IndicatorValue(time=t, indicator="SMA", value=val)
            for t, val in zip(self.times[n:], ma_values)
        ]
    
    def ema(self, n=10):
        """
        Calculates the Exponential Moving Average (EMA) of the close prices.

        Args:
            n (int, optional): The number of periods to use for the moving average. Defaults to 10.

        Returns:
            list: A list of IndicatorValue objects containing the EMA values aligned with their corresponding times.
        """
        # Exponential Moving Average of the close prices.
        ema_values = self.running_ema(self.close, n)
        return [
            IndicatorValue(time=t, indicator="EMA", value=val)
            for t, val in zip(self.times, ema_values)
        ]

    def md(self, n=10):
        """
        Calculates the Moving Deviation (MD) of the close prices.

        Args:
            n (int, optional): The number of periods to use for the moving deviation. Defaults to 10.

        Returns:
            list: A list of IndicatorValue objects containing the MD values aligned with their corresponding times.
        """
        # Rolling standard deviation (moving deviation) of the close prices.
        md_values = self.rolling_std(self.close, n)
        return [
            IndicatorValue(time=t, indicator="MD", value=val)
            for t, val in zip(self.times[n:], md_values)
        ]
    
    def macd(self, fast=12, slow=26, signal=9):
        """
        Calculates the Moving Average Convergence Divergence (MACD) indicator.

        Args:
            fast (int, optional): The number of periods for the fast EMA. Defaults to 12.
            slow (int, optional): The number of periods for the slow EMA. Defaults to 26.
            signal (int, optional): The number of periods for the signal EMA. Defaults to 9.

        Returns:
            list: A list of MACDValue objects containing the MACD, DIF, and DEA values aligned with their corresponding times.
        """
        """
        MACD indicator:
            - DIF = EMA(fast) - EMA(slow)
            - DEA = EMA(signal) of DIF
            - MACD = 2 * (DIF - DEA)
        """
        fast_ema = self.running_ema(self.close, fast)
        slow_ema = self.running_ema(self.close, slow)
        dif = [f - s for f, s in zip(fast_ema, slow_ema)]
        dea = self.running_ema(dif, signal)
        macd_values = [2 * (d - s) for d, s in zip(dif, dea)]
        return [
            MACDValue(time=t, dif=d, dea=s, macd=macd)
            for t, d, s, macd in zip(self.times, dif, dea, macd_values)
        ]
        