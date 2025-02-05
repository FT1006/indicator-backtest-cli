from src.indicators.base import BaseIndicator

class PriceIndicators(BaseIndicator):
    def ma(self, n=10):
        ma_values = self.rolling_mean(self.close, n)
        return list(zip(self.times, ma_values))
    
    def ema(self, n=10):
        ema_values = self.running_ema(self.close, n)
        return list(zip(self.times, ema_values))
    
    def sma(self, n=10):
        sma_values = self.running_sma(self.close, n)
        return list(zip(self.times, sma_values))

    def md(self, n=10):
        md_values = self.rolling_std(self.close, n)
        return list(zip(self.times, md_values))
    
    def macd(self, fast=12, slow=26, signal=9):
        """
        MACD indicator:
          - DIF = EMA(n) - EMA(m)
          - DEA = EMA(k) of DIF
          - MACD = 2 * (DIF - DEA)
        """
        fast_ema = self.running_ema(self.close, fast)
        slow_ema = self.running_ema(self.close, slow)
        dif = [f - s for f, s in zip(fast_ema, slow_ema)]
        dea = self.running_ema(dif, signal)
        macd = [2 * (d - s) for d, s in zip(dif, dea)]
        return list(zip(self.times, macd))
        