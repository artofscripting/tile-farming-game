import random
import time
from constants import seeds_config


class Market:
    def __init__(self):
        """Initialize market with base prices from seed configuration"""
        self.prices = {}
        self.price_trends = {}
        self.last_update = time.time()
        self.update_interval = 30.0  # Update prices every 30 seconds
        
        # Day tracking system
        self.current_day = 1  # Start at day 1
        self.max_days = 180  # Track 180 days
        self.day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Price history tracking
        self.price_history = {}  # {crop_name: [(day, price), ...]}
        self.max_history_length = 180  # Keep 180 days of history
        
        # Initialize prices and trends for each crop
        for seed in seeds_config:
            crop_name = seed['name']
            base_price = seed.get('harvest_price', 10)
            
            # Start with base price plus some random variation (-20% to +20%)
            variation = random.uniform(-0.2, 0.2)
            initial_price = max(1, int(base_price * (1 + variation)))
            self.prices[crop_name] = initial_price
            
            # Initialize price history with starting price
            self.price_history[crop_name] = [(self.current_day, initial_price)]
            
            # Initialize random trend direction
            self.price_trends[crop_name] = random.choice([-1, 0, 1])  # Down, stable, up
        
        # Generate 60 days of historical market data
        self._generate_historical_data(60)
        
        print("Market initialized with dynamic pricing:")
        for crop_name, price in self.prices.items():
            trend_text = "↓" if self.price_trends[crop_name] == -1 else "→" if self.price_trends[crop_name] == 0 else "↑"
            print(f"  {crop_name}: ${price} {trend_text}")
        print(f"Generated 60 days of historical market data (Day {self.current_day - 60} to {self.current_day - 1})")
    
    def _generate_historical_data(self, days_to_generate):
        """Generate historical market data for the specified number of days before current day"""
        print(f"Generating {days_to_generate} days of market history...")
        
        # Save current day and prices
        original_day = self.current_day
        original_prices = self.prices.copy()
        
        # Generate historical data backwards from day 0
        for day_offset in range(days_to_generate, 0, -1):  # Generate days 60, 59, ..., 1 before current day
            historical_day = original_day - day_offset
            
            for crop_name in self.prices.keys():
                current_price = self.prices[crop_name]
                
                # Get base price for this crop
                base_price = 10  # Default
                for seed in seeds_config:
                    if seed['name'] == crop_name:
                        base_price = seed.get('harvest_price', 10)
                        break
                
                # Apply trend-based change (reverse the trend for historical data)
                trend_change = 0
                if self.price_trends[crop_name] == -1:  # Downward trend becomes upward for past
                    trend_change = random.uniform(0.05, 0.15)   # +5% to +15%
                elif self.price_trends[crop_name] == 1:  # Upward trend becomes downward for past
                    trend_change = random.uniform(-0.15, -0.05)  # -5% to -15%
                else:  # Stable trend
                    trend_change = random.uniform(-0.05, 0.05)  # -5% to +5%
                
                # Apply random market volatility
                volatility = random.uniform(-0.1, 0.1)  # Additional ±10% volatility
                
                # Calculate historical price (working backwards)
                total_change = trend_change + volatility
                historical_price = int(current_price / (1 + total_change))
                historical_price = max(1, historical_price)  # Ensure positive price
                
                # Store in history
                self.price_history[crop_name].append((historical_day, historical_price))
                
                # Update current price for next iteration
                self.prices[crop_name] = historical_price
            
            # Occasionally change trend direction for historical consistency
            for crop_name in self.prices.keys():
                if random.random() < 0.2:  # 20% chance to change trend
                    self.price_trends[crop_name] = random.choice([-1, 0, 1])
        
        # Restore original prices and day
        self.prices = original_prices
        self.current_day = original_day
        
        # Sort history by day
        for crop_name in self.price_history:
            self.price_history[crop_name].sort(key=lambda x: x[0])
    
    def update_prices(self):
        """Update market prices based on trends and random fluctuations"""
        current_time = time.time()
        
        if current_time - self.last_update < self.update_interval:
            return  # Not time to update yet
        
        # Advance to next day
        self.current_day += 1
        if self.current_day > self.max_days:
            self.current_day = 1  # Cycle back to day 1 after 180 days
        
        day_of_week = self.get_day_of_week()
        print(f"\n--- Market Update - Day {self.current_day} ({day_of_week}) ---")
        
        for crop_name in self.prices.keys():
            old_price = self.prices[crop_name]
            
            # Get base price for this crop
            base_price = 10  # Default
            for seed in seeds_config:
                if seed['name'] == crop_name:
                    base_price = seed.get('harvest_price', 10)
                    break
            
            # Apply trend-based change
            trend_change = 0
            if self.price_trends[crop_name] == -1:  # Downward trend
                trend_change = random.uniform(-0.15, -0.05)  # -5% to -15%
            elif self.price_trends[crop_name] == 1:  # Upward trend
                trend_change = random.uniform(0.05, 0.15)   # +5% to +15%
            else:  # Stable trend
                trend_change = random.uniform(-0.05, 0.05)  # -5% to +5%
            
            # Apply random market volatility
            volatility = random.uniform(-0.1, 0.1)  # Additional ±10% volatility
            
            # Calculate new price
            total_change = trend_change + volatility
            new_price = int(old_price * (1 + total_change))
            
            # Keep prices within reasonable bounds (50% to 200% of base price)
            min_price = max(1, int(base_price * 0.5))
            max_price = int(base_price * 2.0)
            new_price = max(min_price, min(max_price, new_price))
            
            self.prices[crop_name] = new_price
            
            # Record price in history
            self.price_history[crop_name].append((self.current_day, new_price))
            
            # Keep history length manageable
            if len(self.price_history[crop_name]) > self.max_history_length:
                self.price_history[crop_name] = self.price_history[crop_name][-self.max_history_length:]
            
            # Occasionally change trend direction
            if random.random() < 0.3:  # 30% chance to change trend
                self.price_trends[crop_name] = random.choice([-1, 0, 1])
            
            # Show price change
            if new_price != old_price:
                change = new_price - old_price
                change_text = f"+${change}" if change > 0 else f"${change}"
                trend_text = "↓" if self.price_trends[crop_name] == -1 else "→" if self.price_trends[crop_name] == 0 else "↑"
                print(f"  {crop_name}: ${old_price} → ${new_price} ({change_text}) {trend_text}")
        
        self.last_update = current_time
    
    def update(self, dt):
        """Update method for game loop integration"""
        self.update_prices()
    
    def get_price(self, crop_name):
        """Get current market price for a crop"""
        return self.prices.get(crop_name, 10)  # Default to 10 if crop not found
    
    def get_all_prices(self):
        """Get all current market prices"""
        return self.prices.copy()
    
    def get_price_trend(self, crop_name):
        """Get the current trend for a crop (-1: down, 0: stable, 1: up)"""
        return self.price_trends.get(crop_name, 0)
    
    def get_day_of_week(self):
        """Get the current day of the week name"""
        # Day -61 starts on Monday (index 0)
        # Adjust negative days to positive for modulo calculation
        adjusted_day = self.current_day + 61  # Convert -61 to 0, -60 to 1, etc.
        day_index = adjusted_day % 7
        return self.day_names[day_index]
    
    def get_current_day(self):
        """Get the current day number"""
        return self.current_day
    
    def get_price_history(self, crop_name=None):
        """Get price history for a specific crop or all crops"""
        if crop_name:
            return self.price_history.get(crop_name, [])
        return self.price_history.copy()
    
    def get_market_summary(self):
        """Get a formatted summary of current market conditions"""
        day_of_week = self.get_day_of_week()
        summary = [f"=== Market Prices - Day {self.current_day} ({day_of_week}) ==="]
        for crop_name, price in self.prices.items():
            trend = self.price_trends[crop_name]
            trend_text = "↓ Falling" if trend == -1 else "→ Stable" if trend == 0 else "↑ Rising"
            summary.append(f"{crop_name}: ${price} {trend_text}")
        return "\n".join(summary)

