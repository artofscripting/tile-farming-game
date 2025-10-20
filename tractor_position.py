from constants import grid_size, TILE_OWNED, TILE_TILLED, TILE_READY_HARVEST, TILE_SEED_BIN, TILE_GROWING, TILE_UNOWNED


class TractorPositionChecker:
    """Handles position checking and validation for tractor operations"""
    
    @staticmethod
    def can_start_tilling(x, y, game_window):
        """Check if the tractor can start tilling at a specific position"""
        grid_x = int(x // grid_size) * grid_size
        grid_y = int(y // grid_size) * grid_size
        
        for tile in game_window.farm_tiles:
            if (abs(tile.x - grid_x) < grid_size/2 and 
                abs(tile.y - grid_y) < grid_size/2):
                return tile and (tile.state == TILE_OWNED or tile.state == TILE_TILLED)
        return False
    
    @staticmethod
    def can_till_position(x, y, game_window):
        """Check if there are tillable tiles ahead (for continuation logic)"""
        current_tile_x = int(x // grid_size)
        current_tile_y = int(y // grid_size)
        grid_width = game_window.width // grid_size
        
        # Look ahead in the row starting from the NEXT tile to see if there are any more owned or tilled tiles
        for check_x in range(current_tile_x + 1, grid_width):
            # Find the tile in the game_window.farm_tiles list  
            for tile in game_window.farm_tiles:
                tile_x = int(tile.x // grid_size)
                tile_y = int(tile.y // grid_size)
                if tile_x == check_x and tile_y == current_tile_y:
                    # Continue tilling through owned or already tilled tiles, stop at unowned
                    if tile.state == TILE_OWNED or tile.state == TILE_TILLED:
                        return True  # Found at least one more tile to work on
                    elif tile.state == TILE_UNOWNED:
                        return False  # Hit unowned tile, stop here
                        
        return False  # Reached end of row or no more tillable tiles
    
    @staticmethod
    def can_start_harvesting_position(x, y, game_window):
        """Check if the tractor can start harvesting at the given position (must be ready to harvest)"""
        grid_x = int(x // grid_size) * grid_size
        grid_y = int(y // grid_size) * grid_size
        
        for tile in game_window.farm_tiles:
            if tile.x == grid_x and tile.y == grid_y:
                return tile and tile.state == TILE_READY_HARVEST
        return False
    
    @staticmethod
    def can_harvest_position(x, y, game_window):
        """Check if the tractor can continue harvesting (check if there are any more harvestable tiles ahead)"""
        # Check if there are any harvestable tiles remaining in this row (to the right)
        current_tile_x = int(x // grid_size)
        current_tile_y = int(y // grid_size)
        grid_width = game_window.width // grid_size
        
        # Look ahead in the row starting from the NEXT tile to see if there are any more harvestable tiles
        for check_x in range(current_tile_x + 1, grid_width):
            # Find the tile in the game_window.farm_tiles list
            for tile in game_window.farm_tiles:
                tile_x = int(tile.x // grid_size)
                tile_y = int(tile.y // grid_size)
                if tile_x == check_x and tile_y == current_tile_y and tile.state == TILE_READY_HARVEST:
                    return True  # Found at least one more harvestable tile
                    
        return False  # No more harvestable tiles in this row
    
    @staticmethod
    def has_harvestable_crops_in_row(row_y, game_window, start_x=0):
        """Check if a row has any harvestable crops starting from a specific position"""
        current_tile_y = int(row_y // grid_size)
        start_tile_x = int(start_x // grid_size)
        grid_width = game_window.width // grid_size
        
        # Check if there are any harvestable tiles in this row starting from start_x
        for check_x in range(start_tile_x, grid_width):
            # Find the tile in the game_window.farm_tiles list
            for tile in game_window.farm_tiles:
                tile_x = int(tile.x // grid_size)
                tile_y = int(tile.y // grid_size)
                if tile_x == check_x and tile_y == current_tile_y and tile.state == TILE_READY_HARVEST:
                    return True  # Found at least one harvestable tile in this row
                    
        return False  # No harvestable tiles in this row
    
    @staticmethod
    def can_plant_position(x, y, game_window, seed_type):
        """Check if the tractor can continue planting (check if there are seeds and tilled tiles ahead)"""
        # First check if we have any seeds in seed bins
        if not seed_type:
            return False
            
        # Check if we have seeds available in seed bins
        has_seeds = False
        for bin_tile in game_window.farm_tiles:
            if (bin_tile.state == TILE_SEED_BIN and 
                bin_tile.stored_crop_type == seed_type and 
                bin_tile.stored_amount > 0):
                has_seeds = True
                break
        
        if not has_seeds:
            return False
            
        # Check if there are any tilled tiles remaining in this row (to the right)
        current_tile_x = int(x // grid_size)
        current_tile_y = int(y // grid_size)
        grid_width = game_window.width // grid_size
        
        # Look ahead in the row to see if there are any more tilled tiles
        for check_x in range(current_tile_x, grid_width):
            # Find the tile in the game_window.farm_tiles list
            for tile in game_window.farm_tiles:
                tile_x = int(tile.x // grid_size)
                tile_y = int(tile.y // grid_size)
                if tile_x == check_x and tile_y == current_tile_y and tile.state == TILE_TILLED:
                    return True  # Found at least one tilled tile
                    
        return False  # No tilled tiles in this row
    
    @staticmethod
    def can_start_planting_position(x, y, game_window, seed_type):
        """Check if the tractor can start planting at the given position (must be tilled)"""
        # First check if we have any seeds in seed bins
        if not seed_type:
            return False
            
        # Check if we have seeds available in seed bins
        has_seeds = False
        for bin_tile in game_window.farm_tiles:
            if (bin_tile.state == TILE_SEED_BIN and 
                bin_tile.stored_crop_type == seed_type and 
                bin_tile.stored_amount > 0):
                has_seeds = True
                break
        
        if not has_seeds:
            return False
            
        # Check if the starting position is tilled
        grid_x = int(x // grid_size) * grid_size
        grid_y = int(y // grid_size) * grid_size
        
        start_tile = None
        for tile in game_window.farm_tiles:
            if (abs(tile.x - grid_x) < grid_size/2 and 
                abs(tile.y - grid_y) < grid_size/2):
                start_tile = tile
                break
        
        return start_tile and start_tile.state == TILE_TILLED
    
    @staticmethod
    def can_cultivate_position(x, y, game_window, fertilizer_data):
        """Check if the tractor can apply fertilizer at the current position"""
        grid_x = int(x // grid_size) * grid_size
        grid_y = int(y // grid_size) * grid_size
        
        tile = None
        for t in game_window.farm_tiles:
            if (abs(t.x - grid_x) < grid_size/2 and 
                abs(t.y - grid_y) < grid_size/2):
                tile = t
                break
        
        if not tile:
            return False
        
        # Can cultivate tilled, growing, or harvest-ready tiles
        cultivatable_states = [TILE_TILLED, TILE_GROWING, TILE_READY_HARVEST]
        
        # Check if tile is cultivatable and player can afford fertilizer
        return (tile.state in cultivatable_states and 
                game_window.game_state.can_afford(fertilizer_data['cost']))
    
    @staticmethod
    def can_cultivator_position(x, y, game_window):
        """Check if the tractor can remove weeds at the current position"""
        grid_x = int(x // grid_size) * grid_size
        grid_y = int(y // grid_size) * grid_size
        
        tile = None
        for t in game_window.farm_tiles:
            if (abs(t.x - grid_x) < grid_size/2 and 
                abs(t.y - grid_y) < grid_size/2):
                tile = t
                break
        
        if not tile:
            return False
        
        # Can remove weeds from any farmed tile state (owned, tilled, planted, growing, harvest-ready)
        from constants import TILE_OWNED
        cultivatable_states = [TILE_OWNED, TILE_TILLED, TILE_GROWING, TILE_READY_HARVEST]
        
        # Continue working on any farmed tile regardless of weed count (will work even if weeds are 0)
        return tile.state in cultivatable_states
    
    @staticmethod
    def can_cultivator_continue(x, y, game_window):
        """Check if there are more cultivatable tiles ahead (for continuation logic)"""
        current_tile_x = int(x // grid_size)
        current_tile_y = int(y // grid_size)
        grid_width = game_window.width // grid_size
        
        # Look ahead in the row starting from the NEXT tile to see if there are any more cultivatable tiles
        for check_x in range(current_tile_x + 1, grid_width):
            # Find the tile in the game_window.farm_tiles list  
            for tile in game_window.farm_tiles:
                tile_x = int(tile.x // grid_size)
                tile_y = int(tile.y // grid_size)
                if tile_x == check_x and tile_y == current_tile_y:
                    # Continue through cultivatable tiles, stop at unowned
                    from constants import TILE_OWNED, TILE_UNOWNED
                    cultivatable_states = [TILE_OWNED, TILE_TILLED, TILE_GROWING, TILE_READY_HARVEST]
                    if tile.state in cultivatable_states:
                        return True  # Found at least one more tile to work on
                    elif tile.state == TILE_UNOWNED:
                        return False  # Hit unowned tile, stop here
                        
        return False  # Reached end of row or no more cultivatable tiles

