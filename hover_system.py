"""
Hover System - Handles tile highlighting for buy tiles mode
"""
import pyglet
from constants import grid_size, MOUSE_MODE_BUY_TILES, game_config


class HoverSystem:
    def __init__(self, game_window):
        self.game_window = game_window
        self.hover_tile_x = -1
        self.hover_tile_y = -1
        self.shift_pressed = False
        self.ctrl_pressed = False
    
    def update_hover_position(self, x, y):
        """Update hover tile position for buy tiles mode highlighting"""
        if self.game_window.mouse_mode == MOUSE_MODE_BUY_TILES:
            # Convert mouse coordinates to grid coordinates
            grid_x = int(x // grid_size) * grid_size
            grid_y = int(y // grid_size) * grid_size
            
            # Only track if within the game area (not UI area)
            if (0 <= grid_y < self.game_window.height and 0 <= grid_x < self.game_window.width - 245):
                self.hover_tile_x = grid_x
                self.hover_tile_y = grid_y
            else:
                self.hover_tile_x = -1
                self.hover_tile_y = -1
        else:
            # Reset hover tile when not in buy tiles mode
            self.hover_tile_x = -1
            self.hover_tile_y = -1
    
    def set_shift_pressed(self, pressed):
        """Update shift key state"""
        self.shift_pressed = pressed
    
    def set_ctrl_pressed(self, pressed):
        """Update control key state"""
        self.ctrl_pressed = pressed
    
    def draw_hover_tile_highlight(self):
        """Draw light blue highlight on the tile being hovered over in buy tiles mode"""
        if (self.game_window.mouse_mode == MOUSE_MODE_BUY_TILES and 
            self.hover_tile_x >= 0 and self.hover_tile_y >= 0):
            
            if self.shift_pressed:
                # Highlight all 9 tiles (center + 8 surrounding) if Shift is held and affordable
                self.draw_bulk_tile_highlights()
            elif self.ctrl_pressed:
                # Highlight entire row if Control is held
                self.draw_row_tile_highlights()
            else:
                # Single tile highlight
                hover_highlight = pyglet.shapes.Rectangle(
                    self.hover_tile_x, self.hover_tile_y, grid_size, grid_size,
                    color=(173, 216, 230)  # Light blue color
                )
                hover_highlight.opacity = 100  # Semi-transparent (0-255 scale)
                hover_highlight.draw()
    
    def draw_bulk_tile_highlights(self):
        """Draw highlights for all 9 tiles (center + 8 surrounding) when Shift is held"""
        # Define the 9 tile positions (center + 8 surrounding)
        tile_offsets = [
            (0, 0),                    # Center tile
            (-grid_size, -grid_size),  # Top-left
            (0, -grid_size),           # Top
            (grid_size, -grid_size),   # Top-right
            (-grid_size, 0),           # Left
            (grid_size, 0),            # Right
            (-grid_size, grid_size),   # Bottom-left
            (0, grid_size),            # Bottom
            (grid_size, grid_size)     # Bottom-right
        ]
        
        # Find all tiles that would be affected and check affordability
        tiles_to_highlight = []
        unowned_tiles = []
        
        for offset_x, offset_y in tile_offsets:
            tile_x = self.hover_tile_x + offset_x
            tile_y = self.hover_tile_y + offset_y
            
            # Check if position is within game bounds
            if 0 <= tile_x < self.game_window.width - 245 and 0 <= tile_y < self.game_window.height:
                tile = self.game_window.managers.farm_manager.get_tile_at_position(tile_x, tile_y)
                if tile:
                    tiles_to_highlight.append((tile_x, tile_y))
                    if tile.state == 0:  # TILE_UNOWNED
                        unowned_tiles.append(tile)
        
        # Check if player can afford all unowned tiles
        tile_price = game_config['tile_purchase_price']
        total_cost = len(unowned_tiles) * tile_price
        can_afford = self.game_window.game_state.can_afford(total_cost)
        
        # Choose color based on affordability
        if can_afford and len(unowned_tiles) > 0:
            highlight_color = (173, 216, 230)  # Light blue for affordable
            opacity = 100
        elif len(unowned_tiles) > 0:
            highlight_color = (255, 182, 193)  # Light red for unaffordable
            opacity = 80
        else:
            highlight_color = (220, 220, 220)  # Light gray for no tiles to buy
            opacity = 60
        
        # Draw highlights for all 9 tiles
        for tile_x, tile_y in tiles_to_highlight:
            hover_highlight = pyglet.shapes.Rectangle(
                tile_x, tile_y, grid_size, grid_size,
                color=highlight_color
            )
            hover_highlight.opacity = opacity
            hover_highlight.draw()
    
    def draw_row_tile_highlights(self):
        """Draw highlights for entire row when Control is held"""
        # Find all tiles in the same row (same y coordinate)
        row_y = self.hover_tile_y
        tiles_to_highlight = []
        unowned_tiles = []
        
        # Calculate the row width (game area width minus UI area)
        game_area_width = self.game_window.width - 245
        
        # Go through all tiles in the row
        for tile_x in range(0, game_area_width, grid_size):
            tile = self.game_window.managers.farm_manager.get_tile_at_position(tile_x, row_y)
            if tile:
                tiles_to_highlight.append((tile_x, row_y))
                if tile.state == 0:  # TILE_UNOWNED
                    unowned_tiles.append(tile)
        
        # Check if player can afford all unowned tiles in the row
        tile_price = game_config['tile_purchase_price']
        total_cost = len(unowned_tiles) * tile_price
        can_afford = self.game_window.game_state.can_afford(total_cost)
        
        # Choose color based on affordability
        if can_afford and len(unowned_tiles) > 0:
            highlight_color = (144, 238, 144)  # Light green for affordable row
            opacity = 120
        elif len(unowned_tiles) > 0:
            highlight_color = (255, 182, 193)  # Light red for unaffordable row
            opacity = 80
        else:
            highlight_color = (220, 220, 220)  # Light gray for no tiles to buy in row
            opacity = 60
        
        # Draw highlights for all tiles in the row
        for tile_x, tile_y in tiles_to_highlight:
            hover_highlight = pyglet.shapes.Rectangle(
                tile_x, tile_y, grid_size, grid_size,
                color=highlight_color
            )
            hover_highlight.opacity = opacity
            hover_highlight.draw()

