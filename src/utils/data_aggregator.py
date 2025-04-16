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
        Initializes the DataAggregator with a list of PriceData objects, sorted by their earliest time.

        Args:
            price_data_list (List[PriceData]): A list of PriceData objects to be aggregated.

        Sorting Logic:
            The sorting key is determined as follows:
            - For each PriceData object, its earliest time is used as the sorting key if it has times.
            - If a PriceData object has no times (i.e., it's empty), datetime.max is used to ensure it's sorted last.
            This approach ensures the list is sorted by the earliest time in each PriceData object, allowing for chronological processing of all price points.
        """
        self.price_data_list = sorted(
            price_data_list, 
            key=lambda x: x.get_times()[0] if x.get_times() else datetime.max
        )

    def aggregate_to_timeframe(self, timeframe: str) -> PriceData:
        """
        Aggregates all PricePoint objects in the DataAggregator's price data list into a higher timeframe.

        Parameters:
            timeframe (str): The target aggregation timeframe. Supported values are '5min', '15min', '30min', '1h', '4h', and '1d'.

        Returns:
            PriceData: A new PriceData object containing the aggregated price points at the specified timeframe.

        Raises:
            ValueError: If the specified timeframe is not supported.

        Process Overview:
            1. Validate that the specified timeframe is supported; raise a ValueError if it is not.
            2. Determine the interval size in minutes based on the timeframe.
            3. Create a new PriceData object to store the aggregated results.
            4. Consolidate all PricePoint objects from the price data list into a single list.
            5. If there are no PricePoint objects, return the empty PriceData.
            6. Sort the consolidated PricePoint objects chronologically.
            7. Initialize the first interval by rounding down the earliest timestamp to the nearest interval start.
            8. Iterate through the sorted PricePoints, aggregating those within the same interval.
            9. Process any remaining points in the final interval after iteration.
            10. Return the aggregated PriceData object.
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
        Round down a given datetime to the nearest interval boundary.

        Args:
            time (datetime): The datetime to be normalized.
            interval_minutes (int): The interval in minutes.

        Returns:
            datetime: The normalized datetime.

        Example:
            If time = 10:03 and interval_minutes = 5:
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
        Aggregates a list of PricePoint objects into a single PricePoint representing a candlestick or bar.

        Args:
            points (List[PricePoint]): A list of PricePoint objects to be aggregated.
            timeframe (str): The timeframe of the aggregated PricePoint.

        Returns:
            PricePoint: A single PricePoint object representing the aggregated interval.

        Raises:
            ValueError: If the input list of points is empty.

        This method aggregates a list of PricePoint objects within the same interval into a single PricePoint.
        It ensures the input list is not empty, then calculates the aggregated PricePoint's properties as follows:
        - Open: The open price of the first point in the interval.
        - Close: The close price of the last point in the interval.
        - High: The maximum high price among all points in the interval.
        - Low: The minimum low price among all points in the interval.
        - Volume: The sum of all volumes in the interval.
        - Time: The earliest time in the interval, which is the time of the first point.
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
    This class is responsible for grouping price points into buckets based on a target timeframe (e.g., 5-minute intervals).
    The process involves:
    1. Converting each datetime to seconds since midnight.
    2. Determining which bucket (interval) the time belongs to by integer dividing the total seconds.
    3. Converting back to a datetime representing the start of that bucket.
    4. Grouping price points that fall in the same bucket together.
    5. For each bucket, computing the aggregated Open, High, Low, Close (OHLC) data.

    Attributes:
        target_timeframe (timedelta): The duration of the target timeframe for aggregating price points.
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
        Aggregates price points into higher timeframe bars based on the target timeframe.
        
        This method groups the PricePoint objects from the provided PriceData into buckets 
        according to the target timeframe. It computes the aggregated Open, High, Low, 
        Close (OHLC) data for each bucket and returns a new PriceData object containing 
        the aggregated results.

        Args:
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