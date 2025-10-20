import pyglet
from pyglet import shapes
import math
from constants import seeds_config


class MarketHistoryWindow(pyglet.window.Window):
    def __init__(self, market, game_window=None, *args, **kwargs):
        super().__init__(800, 600, 'Market Price History', resizable=False, *args, **kwargs)
        
        self.market = market
        self.game_window = game_window
        self.selected_crop = None
        self.crop_colors = {}
        self.chart_area = {
            'left': 60,
            'right': self.width - 40,
            'top': self.height - 100,
            'bottom': 80
        }
        
        # Colors
        self.bg_color = (30, 30, 30)
        self.text_color = (255, 255, 255)
        self.grid_color = (60, 60, 60)
        self.axis_color = (150, 150, 150)
        
        # Generate colors for each crop
        self._generate_crop_colors()
        
        # Initially show all crops
        self.visible_crops = set(self.crop_colors.keys())
        
        # Toggle all button properties
        self.toggle_button = {
            'x': self.width - 120,
            'y': self.height - 30,
            'width': 100,
            'height': 25,
            'text': 'Hide All'
        }
        
        # Create title label
        self.title_label = pyglet.text.Label(
            'Market Price History',
            font_name='Arial',
            font_size=18,
            x=self.width // 2,
            y=self.height - 30,
            anchor_x='center',
            anchor_y='center',
            color=self.text_color + (255,)
        )
        
        # Create legend labels
        self.legend_labels = {}
        self._create_legend()
        
        # Update timer - only refresh data every 30 seconds
        self.last_update_time = 0
        self.update_interval = 30.0  # 30 seconds
        self.cached_data = {}  # Cache the filtered history data
        self._update_cached_data()  # Initial data load
    
    def _get_filtered_history(self, crop):
        """Get the last 14 days of price history for a crop"""
        history = self.market.get_price_history(crop)
        if not history:
            return []
        
        # Get the current day from the market
        current_day = self.market.current_day
        
        # Filter to only include the last 14 days
        # Handle day cycling (days cycle from -61 to 180, then back to -61)
        filtered_history = []
        for day, price in history:
            days_ago = current_day - day
            if days_ago < 0:  # Handle day cycling (current day < history day)
                # Days cycle from 180 back to -61, so adjust calculation
                days_ago += (180 - (-61) + 1)  # Total cycle length is 242 days
            
            if days_ago <= 14:  # Include last 14 days
                filtered_history.append((day, price))
        
        # Sort by day to ensure proper order
        filtered_history.sort(key=lambda x: x[0])
        return filtered_history
    
    def _generate_crop_colors(self):
        """Generate distinct colors for each crop"""
        crops = [seed['name'] for seed in seeds_config]
        colors = [
            (255, 100, 100), (100, 255, 100), (100, 100, 255),
            (255, 255, 100), (255, 100, 255), (100, 255, 255),
            (255, 150, 100), (150, 255, 100), (100, 150, 255),
            (255, 100, 150), (100, 255, 150), (150, 100, 255),
            (200, 150, 100), (150, 200, 100), (100, 150, 200),
            (200, 100, 150), (150, 100, 200), (100, 200, 150),
            (180, 180, 100), (180, 100, 180)
        ]
        
        for i, crop in enumerate(crops):
            self.crop_colors[crop] = colors[i % len(colors)]
    
    def _update_cached_data(self):
        """Update cached data for all crops"""
        import time
        self.last_update_time = time.time()
        self.cached_data = {}
        for crop in self.crop_colors.keys():
            self.cached_data[crop] = self._get_filtered_history(crop)
    
    def _should_update_data(self):
        """Check if data should be updated based on timer"""
        import time
        return (time.time() - self.last_update_time) >= self.update_interval
    
    def _create_legend(self):
        """Create legend labels for crops"""
        crops = list(self.crop_colors.keys())
        legend_x = self.width - 200  # Move slightly left to accommodate two columns
        legend_y = self.height - 120
        
        # Clear previous legend labels
        self.legend_labels.clear()
        
        for i, crop in enumerate(crops):
            # Arrange in two columns to fit all crops
            column = i // 13  # 13 crops per column (26 total space, using 20)
            row = i % 13
            
            x_offset = column * 120  # Second column offset
            y_offset = row * 17  # Slightly smaller spacing to fit more
            
            color = self.crop_colors[crop]
            self.legend_labels[crop] = pyglet.text.Label(
                f"● {crop}",
                font_name='Arial',
                font_size=9,  # Slightly smaller font
                x=legend_x + x_offset,
                y=legend_y - y_offset,
                anchor_x='left',
                anchor_y='center',
                color=color + (255,) if crop in self.visible_crops else (100, 100, 100, 255)
            )
    
    def _get_price_range(self):
        """Get the min and max prices across all visible crops (last 14 days)"""
        min_price = float('inf')
        max_price = 0
        
        for crop in self.visible_crops:
            history = self.cached_data.get(crop, [])
            if history:
                prices = [price for day, price in history]
                min_price = min(min_price, min(prices))
                max_price = max(max_price, max(prices))
        
        if min_price == float('inf'):
            return 0, 100
        
        # Add some padding
        padding = (max_price - min_price) * 0.1
        return max(0, min_price - padding), max_price + padding
    
    def _get_day_range(self):
        """Get the min and max days across all crops (last 14 days)"""
        min_day = float('inf')
        max_day = 0
        
        for crop in self.visible_crops:
            history = self._get_filtered_history(crop)
            if history:
                days = [day for day, price in history]
                min_day = min(min_day, min(days))
                max_day = max(max_day, max(days))
        
        if min_day == float('inf'):
            return 1, 30
        
        return min_day, max_day
    
    def _draw_grid_and_axes(self):
        """Draw grid lines and axes"""
        min_price, max_price = self._get_price_range()
        min_day, max_day = self._get_day_range()
        
        chart_width = self.chart_area['right'] - self.chart_area['left']
        chart_height = self.chart_area['top'] - self.chart_area['bottom']
        
        # Draw horizontal grid lines (price levels)
        price_steps = 5
        for i in range(price_steps + 1):
            price = min_price + (max_price - min_price) * i / price_steps
            y = self.chart_area['bottom'] + chart_height * i / price_steps
            
            # Grid line
            line = shapes.Line(
                self.chart_area['left'], y,
                self.chart_area['right'], y,
                color=self.grid_color
            )
            line.draw()
            
            # Price label
            label = pyglet.text.Label(
                f"${int(price)}",
                font_name='Arial',
                font_size=9,
                x=self.chart_area['left'] - 10,
                y=y,
                anchor_x='right',
                anchor_y='center',
                color=self.axis_color + (255,)
            )
            label.draw()
        
        # Draw vertical grid lines (days)
        day_range = max_day - min_day
        if day_range > 0:
            day_steps = min(10, day_range)  # Limit to 10 vertical lines
            for i in range(day_steps + 1):
                day = min_day + (max_day - min_day) * i / day_steps
                x = self.chart_area['left'] + chart_width * i / day_steps
                
                # Grid line
                line = shapes.Line(
                    x, self.chart_area['bottom'],
                    x, self.chart_area['top'],
                    color=self.grid_color
                )
                line.draw()
                
                # Day label
                label = pyglet.text.Label(
                    f"Day {int(day)}",
                    font_name='Arial',
                    font_size=9,
                    x=x,
                    y=self.chart_area['bottom'] - 15,
                    anchor_x='center',
                    anchor_y='center',
                    color=self.axis_color + (255,)
                )
                label.draw()
        
        # Draw axes
        # Y-axis
        y_axis = shapes.Line(
            self.chart_area['left'], self.chart_area['bottom'],
            self.chart_area['left'], self.chart_area['top'],
            color=self.axis_color
        )
        y_axis.draw()
        
        # X-axis
        x_axis = shapes.Line(
            self.chart_area['left'], self.chart_area['bottom'],
            self.chart_area['right'], self.chart_area['bottom'],
            color=self.axis_color
        )
        x_axis.draw()
    
    def _draw_price_lines(self):
        """Draw price history lines for visible crops"""
        min_price, max_price = self._get_price_range()
        min_day, max_day = self._get_day_range()
        
        if max_price == min_price or max_day == min_day:
            return
        
        chart_width = self.chart_area['right'] - self.chart_area['left']
        chart_height = self.chart_area['top'] - self.chart_area['bottom']
        
        for crop in self.visible_crops:
            history = self.cached_data.get(crop, [])
            if len(history) < 2:
                continue
            
            color = self.crop_colors[crop]
            
            # Draw line segments between consecutive points
            for i in range(len(history) - 1):
                day1, price1 = history[i]
                day2, price2 = history[i + 1]
                
                # Convert to screen coordinates
                x1 = self.chart_area['left'] + chart_width * (day1 - min_day) / (max_day - min_day)
                y1 = self.chart_area['bottom'] + chart_height * (price1 - min_price) / (max_price - min_price)
                x2 = self.chart_area['left'] + chart_width * (day2 - min_day) / (max_day - min_day)
                y2 = self.chart_area['bottom'] + chart_height * (price2 - min_price) / (max_price - min_price)
                
                # Draw line segment
                line = shapes.Line(x1, y1, x2, y2, color=color)
                line.draw()
            
            # Draw data points
            for day, price in history:
                # Convert to screen coordinates
                x = self.chart_area['left'] + chart_width * (day - min_day) / (max_day - min_day)
                y = self.chart_area['bottom'] + chart_height * (price - min_price) / (max_price - min_price)
                
                # Draw point
                point = shapes.Circle(x, y, 3, color=color)
                point.draw()
    
    def toggle_crop_visibility(self, crop_name):
        """Toggle the visibility of a crop in the chart"""
        if crop_name in self.visible_crops:
            self.visible_crops.remove(crop_name)
        else:
            self.visible_crops.add(crop_name)
        
        # Update legend colors
        self._create_legend()
    
    def on_draw(self):
        """Render the market history window"""
        # Check if we should update data (every 30 seconds)
        if self._should_update_data():
            self._update_cached_data()
        
        self.clear()
        
        # Draw background
        background = shapes.Rectangle(0, 0, self.width, self.height, color=self.bg_color)
        background.draw()
        
        # Draw title
        self.title_label.draw()
        
        # Draw current day info
        current_day = self.market.get_current_day()
        day_of_week = self.market.get_day_of_week()
        day_info = pyglet.text.Label(
            f"Current: Day {current_day} ({day_of_week})",
            font_name='Arial',
            font_size=12,
            x=self.width // 2,
            y=self.height - 55,
            anchor_x='center',
            anchor_y='center',
            color=(200, 200, 200, 255)
        )
        day_info.draw()
        
        # Draw toggle all button
        btn = self.toggle_button
        button_rect = shapes.Rectangle(
            btn['x'], btn['y'] - btn['height']//2,
            btn['width'], btn['height'],
            color=(70, 70, 70)
        )
        button_rect.draw()
        
        # Draw button border
        border_color = (150, 150, 150)
        border_thickness = 1
        # Create a slightly larger rectangle as border
        button_border = shapes.Rectangle(
            btn['x'] - border_thickness, btn['y'] - btn['height']//2 - border_thickness,
            btn['width'] + 2*border_thickness, btn['height'] + 2*border_thickness,
            color=border_color
        )
        button_border.draw()
        
        button_text = pyglet.text.Label(
            btn['text'],
            font_name='Arial',
            font_size=10,
            x=btn['x'] + btn['width']//2,
            y=btn['y'],
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255)
        )
        button_text.draw()
        
        # Draw chart
        self._draw_grid_and_axes()
        self._draw_price_lines()
        
        # Draw legend
        legend_title = pyglet.text.Label(
            "Crops (click to toggle):",
            font_name='Arial',
            font_size=12,
            x=self.width - 180,
            y=self.height - 100,
            anchor_x='left',
            anchor_y='center',
            color=self.text_color + (255,)
        )
        legend_title.draw()
        
        for label in self.legend_labels.values():
            label.draw()
        
        # Draw instructions
        instructions = pyglet.text.Label(
            "Click on crop names to show/hide them in the chart",
            font_name='Arial',
            font_size=10,
            x=10,
            y=20,
            anchor_x='left',
            anchor_y='center',
            color=(150, 150, 150, 255)
        )
        instructions.draw()
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse clicks for toggling crop visibility"""
        if button == pyglet.window.mouse.LEFT:
            # Check if click is on toggle all button
            btn = self.toggle_button
            if (btn['x'] <= x <= btn['x'] + btn['width'] and 
                btn['y'] - btn['height']/2 <= y <= btn['y'] + btn['height']/2):
                self._toggle_all_crops()
                return
            
            # Check if click is on legend area
            legend_x = self.width - 200
            legend_y_start = self.height - 120
            
            for i, crop in enumerate(self.legend_labels.keys()):
                # Calculate position based on two-column layout
                column = i // 13
                row = i % 13
                
                x_offset = column * 120
                y_offset = row * 17
                
                label_x = legend_x + x_offset
                label_y = legend_y_start - y_offset
                
                if (label_x <= x <= label_x + 115 and 
                    label_y - 8 <= y <= label_y + 8):
                    self.toggle_crop_visibility(crop)
                    break
    
    def _toggle_all_crops(self):
        """Toggle all crops visibility and update button text"""
        if len(self.visible_crops) == len(self.crop_colors):
            self.visible_crops.clear()
            self.toggle_button['text'] = 'Show All'
        else:
            self.visible_crops = set(self.crop_colors.keys())
            self.toggle_button['text'] = 'Hide All'
        self._create_legend()
    
    def on_key_press(self, symbol, modifiers):
        """Handle key presses"""
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
        elif symbol == pyglet.window.key.A:
            # Toggle all crops
            self._toggle_all_crops()
    
    def on_close(self):
        """Handle window close event"""
        # Notify game window that this window is closing
        if self.game_window:
            self.game_window.market_history_window = None
        super().on_close()

