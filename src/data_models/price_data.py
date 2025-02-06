from datetime import datetime

class PricePoint:
    def __init__(self, time, open, high, low, close, volume):
        self.time = time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
    
class PriceData:
    def __init__(self, symbol=None, initial_price=None, initial_time=None):
        self.symbol = symbol
        self.initial_price = initial_price
        self.initial_time = initial_time
        self.price_points = []
        self.variance = None
        
    def add_price_point(self, price_point):
        self.price_points.append(price_point)
        self.last_updated = price_point.time

    def get_latest_price(self):
        return self.price_points[-1].close
    
    def get_price_at_time(self, time):
        for price_point in self.price_points:
            if price_point.time == time:
                return price_point
        return None
    
    def get_price_points_in_timeframe(self, start_time, end_time):
        price_points = []
        for price_point in self.price_points:
            if price_point.time >= start_time and price_point.time <= end_time:
                price_points.append(price_point)
        return price_points

    def calculate_average_price(self):
        if not self.price_points:
            return 0
        total_price = sum(pp.close for pp in self.price_points)
        return total_price / len(self.price_points)

    def get_price_points_count(self):
        return len(self.price_points)