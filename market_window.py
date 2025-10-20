import pyglet
from pyglet import shapes
import time
from constants import seeds_config


class MarketWindow(pyglet.window.Window):
    def __init__(self, market, game_window=None, *args, **kwargs):
        super().__init__(500, 725, 'Live Market Data', resizable=False, *args, **kwargs)
        
        self.market = market
        self.game_window = game_window
        self.labels = {}
        self.price_change_labels = {}
        self.trend_labels = {}
        self.last_prices = {}
        self.price_flash_timers = {}  # For flashing effect on price changes
        self.seed_labels = {}  # For seed price labels
        
        # Colors
        self.bg_color = (40, 40, 40)  # Dark gray background
        self.text_color = (255, 255, 255)  # White text
        self.up_color = (0, 255, 0)  # Green for price increases
        self.down_color = (255, 0, 0)  # Red for price decreases
        self.stable_color = (255, 255, 0)  # Yellow for stable prices
        
        # Create title label
        self.title_label = pyglet.text.Label(
            'Live Market Data',
            font_name='Arial',
            font_size=20,
            x=self.width // 2,
            y=self.height - 30,
            anchor_x='center',
            anchor_y='center',
            color=self.text_color + (255,)
        )
        
        # Create timestamp label with improved initialization
        try:
            self.timestamp_label = pyglet.text.Label(
                'Last Updated: --:--:--',
                font_name='Arial',
                font_size=10,
                x=self.width // 2,
                y=self.height - 55,
                anchor_x='center',
                anchor_y='center',
                color=(200, 200, 200, 255)
            )
        except Exception as e:
            print(f"Warning: Failed to create timestamp label: {e}")
            # Create a simpler fallback label
            self.timestamp_label = pyglet.text.Label(
                'Time: --:--:--',
                font_size=10,
                x=self.width // 2,
                y=self.height - 55,
                anchor_x='center',
                anchor_y='center',
                color=(200, 200, 200, 255)
            )
        
        self.setup_market_labels()
        
        # Schedule updates
        pyglet.clock.schedule_interval(self.update_display, 1.0)  # Update display every second
    
    def setup_market_labels(self):
        """Create labels for each crop in the market"""
        y_start = self.height - 100
        y_spacing = 25
        
        # Create seed price lookup dictionary
        seed_prices = {seed['name']: seed['cost'] for seed in seeds_config}
        
        crop_names = list(self.market.prices.keys())
        
        for i, crop_name in enumerate(crop_names):
            y_pos = y_start - (i * y_spacing)
            
            # Crop name label
            name_label = pyglet.text.Label(
                crop_name,
                font_name='Arial',
                font_size=12,
                x=20,
                y=y_pos,
                anchor_x='left',
                anchor_y='center',
                color=self.text_color + (255,)
            )
            
            # Price label
            price = self.market.get_price(crop_name)
            price_label = pyglet.text.Label(
                f'${price}',
                font_name='Arial',
                font_size=12,
                x=120,
                y=y_pos,
                anchor_x='left',
                anchor_y='center',
                color=self.text_color + (255,)
            )
            
            # Price change label
            change_label = pyglet.text.Label(
                '',
                font_name='Arial',
                font_size=10,
                x=190,
                y=y_pos,
                anchor_x='left',
                anchor_y='center',
                color=self.text_color + (255,)
            )
            
            # Trend label
            trend = self.market.get_price_trend(crop_name)
            trend_text = "↓" if trend == -1 else "→" if trend == 0 else "↑"
            trend_color = self.down_color if trend == -1 else self.stable_color if trend == 0 else self.up_color
            
            trend_label = pyglet.text.Label(
                trend_text,
                font_name='Arial',
                font_size=14,
                x=260,
                y=y_pos,
                anchor_x='center',
                anchor_y='center',
                color=trend_color + (255,)
            )
            
            # Seed price label
            seed_price = seed_prices.get(crop_name, 'N/A')
            seed_price_text = f'${seed_price}' if seed_price != 'N/A' else 'N/A'
            seed_price_label = pyglet.text.Label(
                seed_price_text,
                font_name='Arial',
                font_size=12,
                x=320,
                y=y_pos,
                anchor_x='left',
                anchor_y='center',
                color=(150, 255, 150, 255)  # Light green for seed prices
            )
            
            self.labels[crop_name] = {
                'name': name_label,
                'price': price_label,
                'change': change_label,
                'trend': trend_label,
                'seed_price': seed_price_label
            }
            
            # Store previous price for change tracking (from price history if available)
            history = self.market.price_history.get(crop_name, [])
            if len(history) >= 2:
                # Use the second-to-last price as the "last" price
                self.last_prices[crop_name] = history[-2][1]
            else:
                # Fallback to current price if no history
                self.last_prices[crop_name] = price
            self.price_flash_timers[crop_name] = 0
    

    
    def update_display(self, dt):
        """Update the market display with current data"""
        try:
            current_time = time.strftime("%H:%M:%S")
            # Ensure the timestamp text is properly formatted and encoded
            timestamp_text = f"Last Updated: {current_time}"
            if self.timestamp_label:
                self.timestamp_label.text = timestamp_text
        except Exception as e:
            print(f"Warning: Failed to update timestamp: {e}")
            # Fallback to basic timestamp
            if self.timestamp_label:
                self.timestamp_label.text = "Last Updated: --:--:--"
        
        # Update price flash timers
        for crop_name in self.price_flash_timers:
            if self.price_flash_timers[crop_name] > 0:
                self.price_flash_timers[crop_name] -= dt
        
        # Update each crop's display
        for crop_name in self.labels:
            current_price = self.market.get_price(crop_name)
            last_price = self.last_prices.get(crop_name, current_price)
            
            # Update price label
            self.labels[crop_name]['price'].text = f'${current_price}'
            
            # Update price change if there was a change
            if current_price != last_price:
                change = current_price - last_price
                change_text = f"+${change}" if change > 0 else f"${change}"
                change_color = self.up_color if change > 0 else self.down_color
                
                self.labels[crop_name]['change'].text = change_text
                self.labels[crop_name]['change'].color = change_color + (255,)
                
                # Set flash timer for price label
                self.price_flash_timers[crop_name] = 2.0  # Flash for 2 seconds
                
                # Update stored price
                self.last_prices[crop_name] = current_price
            
            # Update trend
            trend = self.market.get_price_trend(crop_name)
            trend_text = "↓" if trend == -1 else "→" if trend == 0 else "↑"
            trend_color = self.down_color if trend == -1 else self.stable_color if trend == 0 else self.up_color
            
            self.labels[crop_name]['trend'].text = trend_text
            self.labels[crop_name]['trend'].color = trend_color + (255,)
            
            # Apply flash effect to price if timer is active
            if self.price_flash_timers[crop_name] > 0:
                # Alternate between normal and highlighted color
                flash_intensity = int((self.price_flash_timers[crop_name] % 0.5) * 2)
                if flash_intensity:
                    change = current_price - last_price if crop_name in self.last_prices else 0
                    flash_color = self.up_color if change > 0 else self.down_color if change < 0 else self.text_color
                    self.labels[crop_name]['price'].color = flash_color + (255,)
                else:
                    self.labels[crop_name]['price'].color = self.text_color + (255,)
            else:
                self.labels[crop_name]['price'].color = self.text_color + (255,)
    
    def on_draw(self):
        """Render the market window"""
        self.clear()
        
        # Draw background
        background = shapes.Rectangle(0, 0, self.width, self.height, color=self.bg_color)
        background.draw()
        
        # Draw title
        self.title_label.draw()
        
        # Draw timestamp with safety check
        try:
            if self.timestamp_label and hasattr(self.timestamp_label, 'text'):
                self.timestamp_label.draw()
        except Exception as e:
            print(f"Warning: Failed to draw timestamp: {e}")
            # Create a new timestamp label if the current one is corrupted
            try:
                self.timestamp_label = pyglet.text.Label(
                    'Time: --:--:--',
                    font_size=10,
                    x=self.width // 2,
                    y=self.height - 55,
                    anchor_x='center',
                    anchor_y='center',
                    color=(200, 200, 200, 255)
                )
            except:
                pass  # If recreation fails, just skip drawing timestamp
        
        # Draw separator line
        separator = shapes.Line(10, self.height - 70, self.width - 10, self.height - 70, 
                               color=(100, 100, 100))
        separator.draw()
        
        # Draw column headers
        headers = [
            pyglet.text.Label('Crop', font_name='Arial', font_size=10, x=20, y=self.height - 85, 
                            anchor_x='left', anchor_y='center', color=(150, 150, 150, 255)),
            pyglet.text.Label('Price', font_name='Arial', font_size=10, x=120, y=self.height - 85, 
                            anchor_x='left', anchor_y='center', color=(150, 150, 150, 255)),
            pyglet.text.Label('Change', font_name='Arial', font_size=10, x=190, y=self.height - 85, 
                            anchor_x='left', anchor_y='center', color=(150, 150, 150, 255)),
            pyglet.text.Label('Trend', font_name='Arial', font_size=10, x=260, y=self.height - 85, 
                            anchor_x='center', anchor_y='center', color=(150, 150, 150, 255)),
            pyglet.text.Label('Seed Price', font_name='Arial', font_size=10, x=320, y=self.height - 85, 
                            anchor_x='left', anchor_y='center', color=(150, 150, 150, 255))
        ]
        
        for header in headers:
            header.draw()
        
        # Draw all market data labels
        for crop_data in self.labels.values():
            crop_data['name'].draw()
            crop_data['price'].draw()
            crop_data['change'].draw()
            crop_data['trend'].draw()
            crop_data['seed_price'].draw()
    
    def on_close(self):
        """Handle window close event"""
        pyglet.clock.unschedule(self.update_display)
        # Notify game window that this window is closing
        if self.game_window:
            self.game_window.market_window = None
        super().on_close()
    
    def on_key_press(self, symbol, modifiers):
        """Handle key presses"""
        if symbol == pyglet.window.key.ESCAPE:
            self.close()

