# chart_plotting.py
import matplotlib.pyplot as plt
# %matplotlib inline
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def plot_price_data(price_data):
    """Plot price data as candlestick chart with volume subplot.

    Converts PriceData object into a Plotly visualization with:
    - Upper panel: Candlestick chart showing open/high/low/close prices
    - Lower panel: Volume bars showing trading volume

    Args:
        price_data (PriceData): Object containing list of PricePoint objects with:
            - time (datetime)
            - open (float)
            - high (float)
            - low (float)
            - close (float)
            - volume (float)

    Returns:
        None: Displays interactive Plotly chart but doesn't return anything

    Example:
        >>> data = PriceData(symbol="AAPL", price_points=[...])
        >>> plot_price_data(data)
    """
    # Extract lists from price_data.price_points
    times = [pp.time for pp in price_data.price_points]
    opens = [pp.open for pp in price_data.price_points]
    highs = [pp.high for pp in price_data.price_points]
    lows = [pp.low for pp in price_data.price_points]
    closes = [pp.close for pp in price_data.price_points]
    volumes = [pp.volume for pp in price_data.price_points]

    # Build a DataFrame (optional but convenient)
    df = pd.DataFrame({
        'Date': times,
        'Open': opens,
        'High': highs,
        'Low': lows,
        'Close': closes,
        'Volume': volumes,
    })

    # Create a Plotly figure with two rows: the main candlestick chart and the volume bar chart
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.05
    )

    # Candlestick chart for price data
    fig.add_trace(
        go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price'
        ),
        row=1, col=1
    )

    # Volume chart (as bars) in the second row
    fig.add_trace(
        go.Bar(
            x=df['Date'],
            y=df['Volume'],
            name='Volume'
        ),
        row=2, col=1
    )

    # Layout updates
    fig.update_layout(
        title=f"Price Data for {price_data.symbol}",
        xaxis_rangeslider_visible=False
    )

    fig.show()