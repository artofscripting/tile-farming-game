import pyglet
from constants import TILE_BARN, TILE_SEED_BIN, TILE_TILLED, TILE_GROWING, TILE_READY_HARVEST, TILE_OWNED


class TooltipSystem:
    def __init__(self, game_window):
        self.game_window = game_window
        self.tooltip_text = None
        self.tooltip_tile = None
        self.mouse_x = 0
        self.mouse_y = 0
    
    def hide_tooltip(self):
        """Hide the current tooltip"""
        self.tooltip_text = None
        self.tooltip_tile = None
    
    def update_mouse_position(self, x, y):
        """Update mouse position and check for tooltip updates"""
        self.mouse_x = x
        self.mouse_y = y
        
        # Check if mouse is over a building tile for tooltip
        from constants import grid_size
        grid_x = int(x // grid_size) * grid_size
        grid_y = int(y // grid_size) * grid_size
        
        if 0 <= grid_y < self.game_window.height and 0 <= grid_x < self.game_window.width:
            tile = self.game_window.get_tile_at_position(grid_x, grid_y)
            if tile and tile.state in [TILE_BARN, TILE_SEED_BIN, TILE_OWNED, TILE_TILLED, TILE_GROWING, TILE_READY_HARVEST]:
                self.tooltip_tile = tile
                self.update_tooltip_text(tile)
            else:
                self.tooltip_tile = None
                self.tooltip_text = None
        else:
            self.tooltip_tile = None
            self.tooltip_text = None
    
    def update_tooltip_text(self, tile):
        """Update tooltip text based on tile type and contents"""
        if tile.state == TILE_BARN:
            from constants import game_config
            upgrade_cost = game_config['barn_upgrade_cost']
            max_capacity = game_config['barn_upgrade_limit']
            
            capacity_info = f"Capacity: {tile.stored_amount}/{tile.building_capacity}"
            if tile.building_capacity < max_capacity:
                capacity_info += f" (Max: {max_capacity})"
            
            if tile.stored_amount > 0:
                # Get current market price and calculate total value
                current_price = self.game_window.market.get_price(tile.stored_crop_type)
                total_value = current_price * tile.stored_amount
                trend = self.game_window.market.get_price_trend(tile.stored_crop_type)
                trend_text = "↓" if trend == -1 else "→" if trend == 0 else "↑"
                
                self.tooltip_text = f"Barn\nContains: {tile.stored_amount} {tile.stored_crop_type}\nCurrent Price: ${current_price}/unit {trend_text}\nTotal Value: ${total_value}\n{capacity_info}\nLeft-Click: Show info\nShift+Left-Click: Upgrade (${upgrade_cost})\nShift+Right-Click: Sell All"
            else:
                self.tooltip_text = f"Barn\nEmpty\n{capacity_info}\nLeft-Click: Show info\nShift+Left-Click: Upgrade (${upgrade_cost})"
        elif tile.state == TILE_SEED_BIN:
            from constants import game_config
            upgrade_cost = game_config['seed_bin_upgrade_cost']
            max_capacity = game_config['seed_bin_upgrade_limit']
            
            capacity_info = f"Capacity: {tile.stored_amount}/{tile.building_capacity}"
            if tile.building_capacity < max_capacity:
                capacity_info += f" (Max: {max_capacity})"
            
            if tile.stored_amount > 0:
                from constants import seeds_config
                seed_cost = None
                for seed in seeds_config:
                    if seed['name'] == tile.stored_crop_type:
                        seed_cost = seed.get('cost', 0)
                        break
                if seed_cost is None:
                    seed_cost = 0
                seed_price_10 = seed_cost * 10
                self.tooltip_text = f"Seed Bin\nContains: {tile.stored_amount} {tile.stored_crop_type} seeds\nSeed Price: ${seed_cost}/seed\n{capacity_info}\nLeft-Click: Show info\nShift+Left-Click: Upgrade (${upgrade_cost})\nRight-Click: Add 1 seed (${seed_cost})\nShift+Right-Click: Add 10 seeds (${seed_price_10})"
            else:
                self.tooltip_text = f"Seed Bin\nEmpty\n{capacity_info}\nLeft-Click: Show info\nShift+Left-Click: Upgrade (${upgrade_cost})\nRight-Click: Add seeds (price varies by type)\nShift+Right-Click: Add 10 seeds (price varies by type)"
        elif tile.state == TILE_OWNED:
            self.tooltip_text = self._get_nutrient_tooltip("Owned Land", tile)
        elif tile.state == TILE_TILLED:
            self.tooltip_text = self._get_nutrient_tooltip("Tilled Soil", tile)
        elif tile.state == TILE_GROWING:
            crop_info = f"Growing: {tile.crop_type}" if tile.crop_type else "Growing Crop"
            self.tooltip_text = self._get_nutrient_tooltip(crop_info, tile)
        elif tile.state == TILE_READY_HARVEST:
            crop_info = f"Ready to Harvest: {tile.crop_type}" if tile.crop_type else "Ready to Harvest"
            self.tooltip_text = self._get_nutrient_tooltip(crop_info, tile)
    
    def _get_nutrient_tooltip(self, title, tile):
        """Generate nutrient information tooltip for farming tiles"""
        nutrients = tile.nutrients
        tooltip_lines = [title, "Soil Nutrients:"]
        
        # Format nutrients in a readable way
        tooltip_lines.append(f"Nitrogen (N): {nutrients.get('nitrogen', 0)}")
        tooltip_lines.append(f"Phosphorus (P): {nutrients.get('phosphorus', 0)}")
        tooltip_lines.append(f"Potassium (K): {nutrients.get('potassium', 0)}")
        tooltip_lines.append(f"Calcium (Ca): {nutrients.get('calcium', 0)}")
        tooltip_lines.append(f"Magnesium (Mg): {nutrients.get('magnesium', 0)}")
        tooltip_lines.append(f"Sulfur (S): {nutrients.get('sulfur', 0)}")
        tooltip_lines.append(f"Water: {nutrients.get('water', 0)}")
        
        # Add weeds information
        weeds_count = getattr(tile, 'weeds', 0)
        tooltip_lines.append(f"Weeds: {weeds_count}")
        
        return "\n".join(tooltip_lines)
    
    def should_draw(self, show_popups=False):
        """Check if tooltip should be drawn (not over popups)"""
        return self.tooltip_text and self.tooltip_tile and not show_popups
    
    def draw(self):
        """Draw the tooltip if available"""
        if not self.tooltip_text:
            return
            
        # Split tooltip text into lines
        lines = self.tooltip_text.split('\n')
        line_height = 20
        padding = 10
        
        # Calculate tooltip dimensions
        max_width = max(len(line) * 8 for line in lines)  # Rough character width estimation
        tooltip_width = max_width + padding * 2
        tooltip_height = len(lines) * line_height + padding * 2
        
        # Position tooltip near mouse cursor, but keep it on screen
        tooltip_x = self.mouse_x + 15
        tooltip_y = self.mouse_y - tooltip_height - 15
        
        # Keep tooltip on screen
        if tooltip_x + tooltip_width > self.game_window.width:
            tooltip_x = self.mouse_x - tooltip_width - 15
        if tooltip_y < 0:
            tooltip_y = self.mouse_y + 15
            
        # Draw tooltip background
        pyglet.shapes.Rectangle(
            tooltip_x, tooltip_y, tooltip_width, tooltip_height,
            color=(0, 0, 0), batch=None
        ).draw()
        
        pyglet.shapes.Rectangle(
            tooltip_x + 2, tooltip_y + 2, tooltip_width - 4, tooltip_height - 4,
            color=(50, 50, 50), batch=None
        ).draw()
        
        # Draw tooltip text
        for i, line in enumerate(lines):
            label = pyglet.text.Label(
                line,
                x=tooltip_x + padding,
                y=tooltip_y + tooltip_height - padding - (i + 1) * line_height,
                color=(255, 255, 255, 255),
                font_size=12
            )
            label.draw()
    
    def update_tooltip_tick(self):
        """Update tooltip content every tick for dynamic data like market prices"""
        if self.tooltip_tile:
            self.update_tooltip_text(self.tooltip_tile)
    
    def hide_tooltip(self):
        """Hide the current tooltip"""
        self.tooltip_text = None
        self.tooltip_tile = None

