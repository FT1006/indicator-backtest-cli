class BaseIndicator:
    """
    Base class for indicators. It converts the StockData.price_points list into separate
    lists for time, open, high, low, close, and volume. It also provides basic
    rolling and exponential moving average functions.
    """
    def __init__(self, stock_data):
        """
        Initialize the BaseIndicator with stock data.

        Args:
            stock_data (PriceData): The historical price data used for generating indicators.
        """
        self.stock_data = stock_data
        self.times = [p_pt.time for p_pt in stock_data.price_points]
        self.open = [p_pt.open for p_pt in stock_data.price_points]
        self.high = [p_pt.high for p_pt in stock_data.price_points]
        self.low = [p_pt.low for p_pt in stock_data.price_points]
        self.close = [p_pt.close for p_pt in stock_data.price_points]
        self.volume = [p_pt.volume for p_pt in stock_data.price_points]

    def rolling_mean(self, values, n):
        """
        Compute simple (unweighted) moving average over a window of size n.

        Args:
            values (list): The list of values to calculate the moving average.
            n (int): The window size for the moving average.

        Returns:
            list: A list of the moving average values.
        """
        if len(values) < n:
            return None
        return [sum(values[i - n : i]) / n for i in range(n, len(values))]
    
    def rolling_std(self, values, n):
        """
        Compute simple (unweighted) moving standard deviation over a window of size n.

        Args:
            values (list): The list of values to calculate the moving standard deviation.
            n (int): The window size for the moving standard deviation.

        Returns:
            list: A list of the moving standard deviation values.
        """
        if len(values) < n:
            return None
        return [(values[i] - sum(values[i - n : i]) / n) ** 2 for i in range(n, len(values))]
    
    def running_ema(self, values, n, alpha=None):
        """
        Compute exponential moving average over a window of size n.
        If alpha is not given, use the span formula: alpha = 2/(n+1)

        Args:
            values (list): The list of values to calculate the exponential moving average.
            n (int): The window size for the exponential moving average.
            alpha (float, optional): The smoothing factor for the exponential moving average. If not provided, it is calculated using the span formula.

        Returns:
            list: A list of the exponential moving average values.
        """
        if len(values) < n:
            return []
        if alpha is None:
            alpha = 2 / (n + 1)
        ema = [values[0]]
        for v in values[1:]:
            ema.append(ema[-1] + alpha * (v - ema[-1]))
        return ema
    
    def running_sma(self, values, n):
        """
        In our framework we define a “smoothing moving average” (SMA) as an EMA
        with a fixed alpha = 1/n.

        Args:
            values (list): The list of values to calculate the smoothing moving average.
            n (int): The window size for the smoothing moving average.

        Returns:
            list: A list of the smoothing moving average values.
        """
        return self.running_ema(values, n, alpha=1 / n)