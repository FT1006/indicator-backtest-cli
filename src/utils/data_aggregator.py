from typing import List
from datetime import datetime, timedelta
from src.data_models.price_data import PriceData, PricePoint

class DataAggregator: # new
    """
    Aggregates price data from lower timeframes to higher timeframes.
    Supports aggregation to 5min, 15min, 30min, 1h, 4h, and 1d intervals.

    Overview:
    The DataAggregator class is designed to take one or more PriceData objects—each containing multiple PricePoint objects—and aggregate them into a higher timeframe. For example, if you have data in 1-minute intervals but you want 5-minute bars (candles), this class will group points into 5-minute buckets and calculate new open, high, low, close, and volume.
    """

    TIMEFRAME_MINUTES = {
        '5min': 5,
        '15min': 15,
        '30min': 30,
        '1h': 60,
        '4h': 240,
        '1d': 1440
    }

    def __init__(self, price_data_list: List[PriceData]):
        """
        Constructor: __init__
        Purpose: Store a list of PriceData objects in this aggregator.
        Sorting Logic:
        The code calls x.get_times() on each PriceData object.
        If get_times() returns a list of times, it uses the first time x.get_times()[0] as the sorting key.
        If a PriceData object has no times (maybe it’s empty), it uses datetime.max to ensure it sorts to the end.
        This ensures that the list is sorted by the earliest time in each PriceData object. When you later combine all price points, you’ll be dealing with them in chronological order.
        """
        self.price_data_list = sorted(
            price_data_list, 
            key=lambda x: x.get_times()[0] if x.get_times() else datetime.max
        )

    def aggregate_to_timeframe(self, timeframe: str) -> PriceData:
        """
        3. aggregate_to_timeframe Method
        This method does the heavy lifting. Its job is to aggregate all the price points in your DataAggregator’s price data list into a higher timeframe (e.g., 5-minute bars, hourly bars, etc.).
        Validate the Timeframe  
        If you ask for a timeframe that isn’t in TIMEFRAME_MINUTES, it raises an error.
        Get the Interval Size in Minutes  
        For '5min', target_minutes becomes 5. For '1h', target_minutes becomes 60, and so on.
        Create a New PriceData to Store Results  
        We instantiate a fresh PriceData object, intended to hold aggregated points at the new, higher timeframe.
        Combine All PricePoints into One List  
        We loop through each PriceData in self.price_data_list and collect all of their PricePoint objects into a single list.
        Check if There Are Any Points  
        If there are no points at all, just return the empty aggregated_data.
        Sort All Points By Time  
        Now we sort the combined list so that every PricePoint is in ascending time order.
        Initialize the First Interval  
        We pick the time of the earliest point in all_points.
        We then call _normalize_time(...) to round down that time to the nearest “interval start.” (Explained further below.)
        current_interval is a list that will temporarily store points that fall into the same interval.
        Main Loop Over All Points  
        For each PricePoint, we compute interval_end which is start_time + target_minutes.
        Handle the Last Interval  
        After the loop finishes, if there are still points sitting in current_interval, we aggregate them as well.
        Return the Aggregated Result  
        Now aggregated_data contains all the new “candles” or aggregated price bars at the requested timeframe.
        """
        if timeframe not in self.TIMEFRAME_MINUTES:
            raise ValueError(f"Unsupported timeframe. Supported values: {list(self.TIMEFRAME_MINUTES.keys())}")

        target_minutes = self.TIMEFRAME_MINUTES[timeframe]
        aggregated_data = PriceData(timeframe=timeframe)
        
        all_points = []
        for price_data in self.price_data_list:
            all_points.extend(price_data.price_points)
        
        if not all_points:
            return aggregated_data

        all_points.sort(key=lambda x: x.time)
        
        start_time = all_points[0].time
        start_time = self._normalize_time(start_time, target_minutes)
        current_interval = []

        for point in all_points:
            interval_end = start_time + timedelta(minutes=target_minutes)
            
            if point.time < interval_end:
                current_interval.append(point)
            else:
                if current_interval:
                    aggregated_point = self._aggregate_interval(current_interval, timeframe)
                    aggregated_data.add_price_point(aggregated_point)
                
                while point.time >= interval_end:
                    start_time = interval_end
                    interval_end = start_time + timedelta(minutes=target_minutes)
                
                current_interval = [point]

        if current_interval:
            aggregated_point = self._aggregate_interval(current_interval, timeframe)
            aggregated_data.add_price_point(aggregated_point)

        return aggregated_data

    def _normalize_time(self, time: datetime, interval_minutes: int) -> datetime:
        """
        4. _normalize_time Method
        Purpose: Round down a given datetime to the nearest interval boundary.
        How It Works:
        Convert the hour and minute to total minutes from midnight.
        Do integer division by interval_minutes to find how many intervals have passed, then multiply by interval_minutes to get the “rounded down” minute count.
        Rebuild the time object with the new hour and minute, and zero out seconds and microseconds.
        Example: If time = 10:03 and interval_minutes = 5:  
        _normalize_time(10:03, 5) becomes 10:00:00.
        """
        minutes = time.hour * 60 + time.minute
        normalized_minutes = (minutes // interval_minutes) * interval_minutes
        return time.replace(hour=normalized_minutes // 60,
                            minute=normalized_minutes % 60,
                            second=0,
                            microsecond=0)

    def _aggregate_interval(self, points: List[PricePoint], timeframe: str) -> PricePoint:
        """
        5. _aggregate_interval Method
        Purpose: Turn a list of PricePoint objects (all in the same interval) into one “candlestick” or “bar.”
        How It Works:
        We ensure points isn’t empty (just in case).
        Open = the open price of the first point in the interval.
        Close = the close price of the last point in the interval.
        High = the maximum high among the points in that interval.
        Low = the minimum low among the points in that interval.
        Volume = the sum of all volumes in the interval.
        The aggregated candle’s time is set to the earliest time in the interval (points[0].time).
        """
        if not points:
            raise ValueError("Cannot aggregate empty interval")

        interval_start = points[0].time
        
        open_price = points[0].open
        close_price = points[-1].close
        high_price = max(point.high for point in points)
        low_price = min(point.low for point in points)
        total_volume = sum(point.volume for point in points)

        return PricePoint(
            time=interval_start,
            open=open_price,
            high=high_price,
            low=low_price,
            close=close_price,
            volume=total_volume,
            timeframe=timeframe
        )

class TimeframeAggregator: # obsolete
    """
    Bucket Grouping:
    Purpose: The code groups price points into buckets based on a target timeframe (e.g., 5-minute intervals).
    
    Process:
    • Convert each datetime to seconds since midnight.
    • Determine which bucket (interval) the time belongs to by integer dividing the total seconds.
    • Convert back to a datetime representing the start of that bucket.
    • Group price points that fall in the same bucket together.
    • For each bucket, compute the aggregated Open, High, Low, Close (OHLC) data.

    Attributes:
    - target_timeframe (timedelta): The duration of the target timeframe for aggregating price points.
    """

    def __init__(self, target_timeframe: timedelta):
        """
        Constructor: __init__
        Purpose: Initialize the TimeframeAggregator with a target timeframe for aggregation.
        
        Parameters:
        - target_timeframe (timedelta): The duration of the target timeframe for aggregating price points.
        """
        self.target_timeframe = target_timeframe
        raise NotImplementedError("TimeframeAggregator is obsolete. Use DataAggregator instead.")

    def aggregate(self, price_data: PriceData) -> PriceData:
        """
        Aggregate price points into higher timeframe bars based on the target timeframe.
        
        This method groups the PricePoint objects from the provided PriceData into buckets 
        according to the target timeframe. It computes the aggregated Open, High, Low, 
        Close (OHLC) data for each bucket and returns a new PriceData object containing 
        the aggregated results.

        Parameters:
        - price_data (PriceData): The PriceData object containing the price points to be aggregated.

        Returns:
        - PriceData: A new PriceData object containing the aggregated price points.
        """
        aggregated = PriceData(symbol=price_data.symbol, 
                               initial_price=price_data.initial_price,
                               initial_time=price_data.initial_time)
        # Group PricePoints into buckets based on target_timeframe.
        groups = {}
        for pp in price_data.price_points:
            # Create a bucket time by “rounding down” the current time to the target interval.
            # (This is a simplified example; in production you’d need to handle timezones, etc.)
            bucket_seconds = (pp.time.hour * 3600 + pp.time.minute * 60 +
                              pp.time.second) // self.target_timeframe.seconds * self.target_timeframe.seconds
            bucket_time = datetime(pp.time.year, pp.time.month, pp.time.day) + timedelta(seconds=bucket_seconds)
            groups.setdefault(bucket_time, []).append(pp)

        # For each group, compute aggregated OHLC data.
        for bucket_time in sorted(groups.keys()):
            points = groups[bucket_time]
            aggregated_point = PricePoint(
                time=bucket_time,
                open=points[0].open,               # open of first bar
                high=max(p.high for p in points),    # highest high
                low=min(p.low for p in points),      # lowest low
                close=points[-1].close,              # close of last bar
                volume=sum(p.volume for p in points) # total volume
            )
            aggregated.add_price_point(aggregated_point)
        return aggregated