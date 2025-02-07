from dataclasses import dataclass
from datetime import datetime

@dataclass
class ordersignal:
    time: datetime
    action: str  # 'BUY' or 'SELL'
    price: float
    strategy: str