"""
Purchase handling for buying tiles
"""
from constants import grid_size, game_config


class PurchaseHandler:
    """Handles tile purchasing operations"""
    
    def __init__(self, game_window):
        self.game_window = game_window
    
    def buy_surrounding_tiles(self, center_tile, center_x, center_y):
        """Buy all 8 surrounding tiles if they are unowned and player has enough money"""
        # Define the 8 surrounding positions (relative to center tile)
        surrounding_offsets = [
            (-grid_size, -grid_size),  # Top-left
            (0, -grid_size),           # Top
            (grid_size, -grid_size),   # Top-right
            (-grid_size, 0),           # Left
            (grid_size, 0),            # Right
            (-grid_size, grid_size),   # Bottom-left
            (0, grid_size),            # Bottom
            (grid_size, grid_size)     # Bottom-right
        ]
        
        unowned_tiles = []
        
        # First, find all unowned surrounding tiles
        for offset_x, offset_y in surrounding_offsets:
            tile_x = center_x + offset_x
            tile_y = center_y + offset_y
            
            # Check if position is within game bounds
            if 0 <= tile_x < self.game_window.width - 245 and 0 <= tile_y < self.game_window.height:
                surrounding_tile = self.game_window.get_tile_at_position(tile_x, tile_y)
                if surrounding_tile and surrounding_tile.state == 0:  # TILE_UNOWNED
                    unowned_tiles.append(surrounding_tile)
        
        # Include the center tile in purchase if it's unowned
        if center_tile.state == 0:  # TILE_UNOWNED
            unowned_tiles.append(center_tile)
        
        # Calculate total cost
        tile_price = game_config['tile_purchase_price']
        total_cost = len(unowned_tiles) * tile_price
        
        # Check if player can afford all tiles
        if len(unowned_tiles) == 0:
            print("No unowned tiles to purchase in the surrounding area!")
            return
            
        if not self.game_window.game_state.can_afford(total_cost):
            print(f"Cannot afford to buy {len(unowned_tiles)} tiles (${total_cost} needed, have ${self.game_window.game_state.money})")
            return
        
        # Purchase all unowned tiles
        if self.game_window.game_state.spend_money(total_cost):
            for tile in unowned_tiles:
                tile.set_state(1)  # TILE_OWNED
            
            print(f"Purchased {len(unowned_tiles)} tiles for ${total_cost} (${tile_price} each)")
        else:
            print(f"Failed to purchase tiles (insufficient funds)")
    
    def buy_entire_row(self, center_tile, center_x, center_y):
        """Buy all unowned tiles in the entire row if player has enough money"""
        row_y = center_y
        unowned_tiles = []
        
        # Calculate the row width (game area width minus UI area)
        game_area_width = self.game_window.width - 245
        
        # Go through all tiles in the row
        for tile_x in range(0, game_area_width, grid_size):
            tile = self.game_window.managers.farm_manager.get_tile_at_position(tile_x, row_y)
            if tile and tile.state == 0:  # TILE_UNOWNED
                unowned_tiles.append(tile)
        
        # Calculate total cost
        tile_price = game_config['tile_purchase_price']
        total_cost = len(unowned_tiles) * tile_price
        
        # Check if player can afford all tiles
        if len(unowned_tiles) == 0:
            print("No unowned tiles to purchase in this row!")
            return
            
        if not self.game_window.game_state.can_afford(total_cost):
            print(f"Cannot afford to buy {len(unowned_tiles)} tiles in row (${total_cost} needed, have ${self.game_window.game_state.money})")
            return
        
        # Purchase all unowned tiles in the row
        if self.game_window.game_state.spend_money(total_cost):
            for tile in unowned_tiles:
                tile.set_state(1)  # TILE_OWNED
            
            print(f"Purchased entire row: {len(unowned_tiles)} tiles for ${total_cost} (${tile_price} each)")
        else:
            print(f"Failed to purchase row tiles (insufficient funds)")

