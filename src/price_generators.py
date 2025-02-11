import random
import math
from datetime import timedelta, datetime
from src.data_models.price_data import PriceData, PricePoint
from abc import ABC, abstractmethod

class PriceBaseGenerator(ABC):
    """Abstract base class for generating minute-level stock prices.
    
    Subclasses must implement the generate_minute_price method to define specific
    price generation logic.
    
    Args:
        ABC (ABC): Inherits from ABC to make this an abstract base class
    """
    @abstractmethod
    def generate_minute_price(self, stock_data, time):
        """Generate and add new price point to StockData.
        
        Args:
            stock_data (PriceData): Stock data object to update
            time (datetime): Timestamp for the new price point
            
        Returns:
            None: Updates StockData in-place
        """
        pass

    def update_stock_data(self, stock_data, open_price, close_price):
        # Create OHLCV data for the minute
        # For simplicity, assume open == close, high & low ~ small random
        time = stock_data.last_updated + timedelta(minutes=1)
        high_price = max(open_price, close_price) + random.uniform(0, self.volatility)
        low_price = min(open_price, close_price) - random.uniform(0, self.volatility)
        volume = random.randint(100, 1000)

        # Update the StockData object with the new price point
        stock_data.add_price_point(
            PricePoint(
                time, 
                open_price, 
                high_price, 
                low_price, 
                close_price, 
                volume
            )
        )

# gen method 1: random walk
class RandomWalkGenerator(PriceBaseGenerator):
    """Generates stock prices using a random walk model with daily drift.
    
    Attributes:
        volatility (float): Maximum percentage change per minute (0-1). Defaults to 0.03.
        drift (float): Daily price drift magnitude (absolute value). Defaults to 0.05.
        last_price (float): Last recorded price for continuity between generations.
    """
    def __init__(self, volatility=0.03, drift=0.05):
        """Initialize random walk generator.
        
        Args:
            volatility (float, optional): Maximum percentage change per minute. Defaults to 0.03.
            drift (float, optional): Daily price drift magnitude. Defaults to 0.05.
        """
        self.volatility = volatility
        self.drift = drift
        self.last_price = None
    
    def generate_minute_price(self, stock_data: PriceData):
        """Generate next price using random walk model with daily drift.
        
        Implementation steps:
        1. Get latest price from stock data
        2. Generate random price fluctuation within volatility bounds
        3. Apply daily drift at market open (first minute of trading day)
        4. Update stock data with new price point
        
        Args:
            stock_data (PriceData): Stock data object to update with new price point
            
        Returns:
            None: Updates PriceData object in-place via update_stock_data()
        """
        if self.last_price is None:
            self.last_price = stock_data.get_latest_price()

        fluctuation = random.uniform(-self.volatility, self.volatility)

        new_price = self.last_price + fluctuation
        if stock_data.get_price_points_count() == 0 or stock_data.get_price_points_count() % 390 == 0: # Every 390 minutes (1 trading day)
            new_price += random.uniform(-self.drift, self.drift)
        
        open_price = self.last_price
        close_price = new_price

        # Update the StockData object with the new price point
        self.update_stock_data(stock_data, open_price, close_price)

# gen method 2: Geometric Brownian Motion (GBM)
class GeometricBrownianMotionPriceGenerator(PriceBaseGenerator):
    """Generates stock prices using Geometric Brownian Motion (GBM) model.
    
    Implements the classic Black-Scholes model for stock price evolution.
    """
    def __init__(self, volatility=0.03, drift=0.05, mu=0.1, sigma=0.2):
        """Initialize GBM generator.
        
        Args:
            volatility (float, optional): Base volatility component. Defaults to 0.03.
            drift (float, optional): Daily drift component. Defaults to 0.05.
            mu (float, optional): Annual expected return (drift). Defaults to 0.1.
            sigma (float, optional): Annual volatility. Defaults to 0.2.
        """
        self.mu = mu
        self.sigma = sigma
        self.last_price = None
        self.volatility = volatility 
        self.drift = drift

        # One minute as a fraction of a year (roughly 525,600 minutes per year)
        self.dt = 1.0 / 525600.0

    def generate_minute_price(self, stock_data: PriceData):
        """Calculate next price using Geometric Brownian Motion (GBM) formula.
        
        Implements the discretized version of the solution to the SDE:
        S_{t+1} = S_t * exp((μ - σ²/2)Δt + σ√Δt Z)
        
        Implementation steps:
        1. Draw random normal variable for Brownian motion
        2. Calculate drift and diffusion terms
        3. Compute new price using GBM formula
        4. Apply daily drift component at market open
        5. Update stock data with new price point
        
        Args:
            stock_data (PriceData): Stock data object to update with new price point
            
        Returns:
            None: Updates PriceData object in-place via update_stock_data()
        """
        self.last_price = stock_data.get_latest_price()

        # Draw from a normal distribution
        z = random.gauss(0, 1)

        drift_term = (self.mu - 0.5 * self.sigma ** 2) * self.dt
        diffusion_term = self.sigma * math.sqrt(self.dt) * z

        new_price = self.last_price * math.exp(drift_term + diffusion_term)

        if stock_data.get_price_points_count() == 0 or stock_data.get_price_points_count() % 390 == 0: # Every 390 minutes (1 trading day)
            new_price = self.last_price * math.exp(drift_term + diffusion_term) + random.uniform(-self.drift, self.drift)
        
        open_price = self.last_price
        close_price = new_price

        # Update the StockData object with the new price point
        self.update_stock_data(stock_data, open_price, close_price)

# gen method 3: Heston Jump Diffusion Model
class HestonJumpDiffusionPriceGenerator(PriceBaseGenerator):
    """Generates stock prices using Heston model with jump diffusion.
    
    Combines stochastic volatility (Heston model) with Merton-style jumps. Models asset prices with
    mean-reverting stochastic volatility and occasional log-normal jumps.
    
    Attributes:
        mu (float): Risk-neutral drift rate (annualized). Defaults to 0.1.
        kappa (float): Mean reversion speed for variance. Defaults to 1.5.
        theta (float): Long-run variance level. Defaults to 0.04.
        sigma_v (float): Volatility of variance process. Defaults to 0.3.
        rho (float): Correlation between price and variance Brownian motions. Defaults to 0.0.
        jump_lambda (float): Annualized jump arrival rate. Defaults to 0.001.
        jump_mean (float): Mean of log jump size. Defaults to -0.2.
        jump_vol (float): Volatility of jump size. Defaults to 0.3.
        dt (float): Time step size (1 minute as fraction of year). Calculated as 1/525600.
        last_price (float): Last generated price for continuity between steps.
        volatility (float): Base volatility component. Defaults to 0.03.
        drift (float): Daily drift component. Defaults to 0.05.
    """
    def __init__(self, volatility=0.03, drift=0.05, mu=0.1, kappa=1.5, theta=0.04, 
                 sigma_v=0.3, rho=0.0, jump_lambda=0.001, jump_mean=-0.2, jump_vol=0.3):
        """Initialize Heston model with jumps.
        
        Args:
            volatility (float, optional): Base volatility. Defaults to 0.03.
            drift (float, optional): Daily drift component. Defaults to 0.05.
            mu (float, optional): Risk-neutral drift rate. Defaults to 0.1.
            kappa (float, optional): Mean reversion speed of variance. Defaults to 1.5.
            theta (float, optional): Long-run variance. Defaults to 0.04.
            sigma_v (float, optional): Volatility of variance. Defaults to 0.3.
            rho (float, optional): Correlation between price and variance. Defaults to 0.0.
            jump_lambda (float, optional): Jump arrival rate. Defaults to 0.001.
            jump_mean (float, optional): Mean jump size. Defaults to -0.2.
            jump_vol (float, optional): Jump size volatility. Defaults to 0.3.
        """
        self.mu = mu           # Drift
        self.kappa = kappa     # Mean reversion speed of variance
        self.theta = theta     # Long-run variance
        self.sigma_v = sigma_v # Vol of variance
        self.rho = rho         # Correlation
        self.jump_lambda = jump_lambda
        self.jump_mean = jump_mean
        self.jump_vol = jump_vol
        self.dt = 1.0 / 525600.0  # 1 minute fraction of a year  
        self.last_price = None
        self.volatility = volatility 
        self.drift = drift

    def generate_minute_price(self, stock_data: PriceData):
        """Generate next price using Heston model with jump diffusion.
        
        Implements the following steps:
        1. Draw correlated random variables for price and variance processes
        2. Update variance process using Heston's stochastic volatility model
        3. Calculate price diffusion component
        4. Check for and apply jumps using Poisson process
        5. Apply daily drift component at market open
        6. Update stock data with new price point
        
        Args:
            stock_data (PriceData): Stock data object to update with new price point
            
        Returns:
            None: Updates PriceData object in-place via update_stock_data()
        """
        self.last_price = stock_data.get_latest_price()

        stock_data.variance = 0.04  # e.g., 20% vol squared
        v = stock_data.variance

        # Draw correlated randoms (z1 for price, z2 for variance)
        z1 = random.gauss(0, 1)
        z2 = random.gauss(0, 1)
        if self.rho != 0.0:
            z2 = self.rho * z1 + math.sqrt(1 - self.rho**2) * z2

        # Update variance (Heston)
        dv = self.kappa * (self.theta - v) * self.dt + \
             self.sigma_v * math.sqrt(max(v, 0.0)) * math.sqrt(self.dt) * z2
        new_v = max(v + dv, 0.0)
        stock_data.variance = new_v

        # Price diffusion
        dS_diffusion = self.mu * self.last_price * self.dt + \
                       math.sqrt(max(v, 0.0)) * self.last_price * math.sqrt(self.dt) * z1
        new_price = self.last_price + dS_diffusion

        # Jump check (Poisson process)
        jump_prob = 1 - math.exp(-self.jump_lambda * self.dt)
        if random.random() < jump_prob:
            # Merton-style lognormal jump
            z_jump = random.gauss(0, 1)
            jump_factor = math.exp(self.jump_mean + self.jump_vol * z_jump)
            new_price *= jump_factor

        # Final guard check
        new_price = max(new_price, 0.01)
        if stock_data.get_price_points_count() == 0 or stock_data.get_price_points_count() % 390 == 0: # Every 390 minutes (1 trading day)
            new_price += random.uniform(-self.drift, self.drift)

        open_price = self.last_price
        close_price = new_price

        # Update the StockData object with the new price point
        self.update_stock_data(stock_data, open_price, close_price)
    