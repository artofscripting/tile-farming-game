from constants import (
    grid_size, TILE_OWNED, TILE_TILLED, TILE_READY_HARVEST, TILE_BARN, 
    TILE_SEED_BIN, TILE_GROWING
)
from tractor_position import TractorPositionChecker
from tractor_operations import TractorOperations


class TractorMultiRow:
    """Handles multi-row tractor operations"""
    
    def __init__(self, tractor_core):
        self.tractor = tractor_core
        self.position_checker = TractorPositionChecker()
        self.operations = TractorOperations(tractor_core)
    
    # Multi-row position methods (work on all active rows simultaneously)
    def till_current_position_multi_row(self, game_window):
        """Till at current position on all active rows"""
        if hasattr(self.tractor, 'active_rows') and self.tractor.active_rows:
            for row_y in self.tractor.active_rows:
                tile = self.tractor.get_tile_at_position(self.tractor.sprite.x, row_y, game_window)
                if tile and tile.state == TILE_OWNED:
                    tile.set_state(TILE_TILLED)
        else:
            # Fallback to single row
            self.operations.till_current_position(game_window)
    
    def plant_current_position_multi_row(self, game_window):
        """Plant at current position on all active rows - one seed per tile"""
        if hasattr(self.tractor, 'active_rows') and self.tractor.active_rows and self.tractor.selected_seed:
            # Plant on each row only if the tile is tilled and we have seeds in bins
            for row_y in self.tractor.active_rows:
                tile = self.tractor.get_tile_at_position(self.tractor.sprite.x, row_y, game_window)
                if tile and tile.state == TILE_TILLED:
                    # Find a seed bin with the selected seed type
                    seed_bin = None
                    for bin_tile in game_window.farm_tiles:
                        if (bin_tile.state == TILE_SEED_BIN and 
                            bin_tile.stored_crop_type == self.tractor.selected_seed and 
                            bin_tile.stored_amount > 0):
                            seed_bin = bin_tile
                            break
                    
                    if seed_bin:
                        # Use one seed from the bin per tile
                        seed_bin.stored_amount -= 1
                        tile.plant_crop(self.tractor.selected_seed)
                    else:
                        # No more seeds in bins, stop planting completely
                        print(f"Out of {self.tractor.selected_seed} seeds in seed bins!")
                        self.tractor.process_job_completion(game_window)
                        self.tractor.moving = False
                        self.tractor.hide()
                        return
        else:
            # Fallback to single row
            self.operations.plant_current_position(game_window)
    
    def harvest_current_position_multi_row(self, game_window):
        """Harvest at current position on all active rows"""
        if hasattr(self.tractor, 'active_rows') and self.tractor.active_rows:
            for row_y in self.tractor.active_rows:
                tile = self.tractor.get_tile_at_position(self.tractor.sprite.x, row_y, game_window)
                if tile and tile.state == TILE_READY_HARVEST:
                    # Harvest the crop (now returns crop_name and amount)
                    crop_name, amount = tile.harvest()
                    if crop_name:
                        # Try to store in nearest barn, otherwise sell for money
                        stored = False
                        for barn_tile in game_window.farm_tiles:
                            if barn_tile.state == TILE_BARN and barn_tile.can_store_crop(crop_name):
                                amount_stored = barn_tile.store_crop(crop_name, amount)
                                if amount_stored > 0:
                                    stored = True
                                    print(f"Stored {amount} {crop_name} in barn")
                                    break
                        
                        # Add to harvest accumulator instead of immediate sale/transaction
                        market_price = game_window.market.get_price(crop_name)
                        self.tractor.add_to_harvest_accumulator(crop_name, amount, stored, market_price)
                        
                        if stored:
                            print(f"Tractor harvested {amount} {crop_name} - stored in barn")
                        else:
                            print(f"Tractor harvested {amount} {crop_name} - will be sold at job completion for ${market_price} each (market price)")
        else:
            # Fallback to single row
            self.operations.harvest_current_position(game_window)
    
    def cultivate_current_position_multi_row(self, game_window):
        """Cultivate at current position on all active rows"""
        if hasattr(self.tractor, 'active_rows') and self.tractor.active_rows and hasattr(self.tractor, 'selected_fertilizer') and self.tractor.selected_fertilizer:
            for row_y in self.tractor.active_rows:
                tile = self.tractor.get_tile_at_position(self.tractor.sprite.x, row_y, game_window)
                if tile:
                    # Create unique identifier for this tile position
                    tile_id = (int(tile.x // grid_size), int(tile.y // grid_size))
                    
                    # Only process if we haven't cultivated this tile yet
                    if tile_id not in self.tractor.cultivated_tiles and self.position_checker.can_cultivate_position(self.tractor.sprite.x, row_y, game_window, self.tractor.selected_fertilizer):
                        # Mark this tile as cultivated
                        self.tractor.cultivated_tiles.add(tile_id)
                        
                        # Apply fertilizer
                        fertilizer = self.tractor.selected_fertilizer
                        
                        # Add to fertilizer cost accumulator (payment will be processed at job completion)
                        self.tractor.add_to_fertilizer_accumulator(fertilizer['name'], fertilizer['cost'])
                        
                        # Apply nutrients from fertilizer to tile
                        nutrient_keys = ['nitrogen', 'phosphorus', 'potassium', 'calcium', 'magnesium', 'sulfur', 'water']
                        for nutrient in nutrient_keys:
                            if nutrient in fertilizer and hasattr(tile, 'nutrients') and nutrient in tile.nutrients:
                                amount = fertilizer[nutrient]
                                if amount > 0:
                                    tile.nutrients[nutrient] += amount
                        
                        tile.update_visual_appearance()
        else:
            # Fallback to single row
            self.operations.cultivate_current_position(game_window)
    
    def cultivate_weeds_current_position_multi_row(self, game_window):
        """Remove weeds at current position on all active rows"""
        if hasattr(self.tractor, 'active_rows') and self.tractor.active_rows:
            for row_y in self.tractor.active_rows:
                tile = self.tractor.get_tile_at_position(self.tractor.sprite.x, row_y, game_window)
                if tile:
                    # Create unique identifier for this tile position
                    tile_id = (int(tile.x // grid_size), int(tile.y // grid_size))
                    
                    # Only process if we haven't worked on this tile yet
                    if tile_id not in self.tractor.cultivated_tiles and self.position_checker.can_cultivator_position(self.tractor.sprite.x, row_y, game_window):
                        # Mark this tile as worked on
                        self.tractor.cultivated_tiles.add(tile_id)
                        
                        # Remove weeds (works even if weeds are already 0)
                        if tile.cultivate_weeds():
                            print(f"🚜 Multi-row tractor removed weeds at ({tile.x}, {tile.y})")
                        else:
                            print(f"🚜 Multi-row tractor processed tile at ({tile.x}, {tile.y}) - no weeds found")
        else:
            # Fallback to single row
            self.operations.cultivate_weeds_current_position(game_window)
    
    # Multi-row operation methods
    def start_tilling_multi_row(self, base_row_y, field_width, game_window, start_x=0, num_rows=1):
        """Start tilling multiple rows"""
        # Clear any previous active rows to prevent carryover from previous operations
        self.tractor.active_rows = []
        
        if num_rows == 1:
            return self.operations.start_tilling_row(base_row_y, field_width, game_window, start_x)
        
        # For 3-row mode, till the clicked row and one above/below if available and owned
        rows_to_till = []
        
        # Add row above if available, owned, and can be tilled
        if base_row_y - grid_size >= 0:
            if self.position_checker.can_start_tilling(start_x, base_row_y - grid_size, game_window):
                rows_to_till.append(base_row_y - grid_size)
        
        # Add the clicked row (base row)
        rows_to_till.append(base_row_y)
        
        # Add row below if available, owned, can be tilled, and we need more rows
        if len(rows_to_till) < num_rows and base_row_y + grid_size < game_window.height:
            if self.position_checker.can_start_tilling(start_x, base_row_y + grid_size, game_window):
                rows_to_till.append(base_row_y + grid_size)
        
        # Set up all rows to work on simultaneously
        self.tractor.active_rows = rows_to_till
        if len(rows_to_till) > 1:
            print(f"🚜 3-row tilling: working on {len(rows_to_till)} rows simultaneously")
        
        # Start with the base row (tractor sprite position)
        success = self.operations.start_tilling_row(base_row_y, field_width, game_window, start_x)
        return success
    
    def start_planting_multi_row(self, base_row_y, field_width, game_window, start_x=0, seed_type=None, num_rows=1):
        """Start planting multiple rows"""
        # Clear any previous active rows to prevent carryover from previous operations
        self.tractor.active_rows = []
        
        if num_rows == 1:
            return self.operations.start_planting_row(base_row_y, field_width, game_window, start_x, seed_type)
        
        # For 3-row mode, plant the clicked row and one above/below if available, tilled, and can be planted
        rows_to_plant = []
        
        # Add row above if available, tilled, and can be planted
        if base_row_y - grid_size >= 0:
            if self.position_checker.can_start_planting_position(start_x, base_row_y - grid_size, game_window, seed_type):
                rows_to_plant.append(base_row_y - grid_size)
        
        # Add the clicked row (base row)
        rows_to_plant.append(base_row_y)
        
        # Add row below if available, tilled, can be planted, and we need more rows
        if len(rows_to_plant) < num_rows and base_row_y + grid_size < game_window.height:
            if self.position_checker.can_start_planting_position(start_x, base_row_y + grid_size, game_window, seed_type):
                rows_to_plant.append(base_row_y + grid_size)
        
        # Set up all rows to work on simultaneously
        self.tractor.active_rows = rows_to_plant
        if len(rows_to_plant) > 1:
            print(f"🚜 3-row planting: working on {len(rows_to_plant)} rows simultaneously")
        
        # Start with the base row (tractor sprite position)
        success = self.operations.start_planting_row(base_row_y, field_width, game_window, start_x, seed_type)
        return success
    
    def start_harvesting_multi_row(self, base_row_y, field_width, game_window, start_x=0, num_rows=1):
        """Start harvesting multiple rows"""
        # Clear any previous active rows to prevent carryover from previous operations
        self.tractor.active_rows = []
        
        if num_rows == 1:
            return self.operations.start_harvesting_row(base_row_y, field_width, game_window, start_x)
        
        # For 3-row mode, harvest the clicked row and one above/below if available and have harvestable crops
        rows_to_harvest = []
        
        # Add row above if available and has harvestable crops
        if base_row_y - grid_size >= 0:
            if self.position_checker.has_harvestable_crops_in_row(base_row_y - grid_size, game_window, start_x):
                rows_to_harvest.append(base_row_y - grid_size)
        
        # Add the clicked row (base row)
        rows_to_harvest.append(base_row_y)
        
        # Add row below if available, has harvestable crops, and we need more rows
        if len(rows_to_harvest) < num_rows and base_row_y + grid_size < game_window.height:
            if self.position_checker.has_harvestable_crops_in_row(base_row_y + grid_size, game_window, start_x):
                rows_to_harvest.append(base_row_y + grid_size)
        
        # Set up all rows to work on simultaneously
        self.tractor.active_rows = rows_to_harvest
        if len(rows_to_harvest) > 1:
            print(f"🚜 3-row harvesting: working on {len(rows_to_harvest)} rows simultaneously")
        
        # Start with the base row (tractor sprite position)
        success = self.operations.start_harvesting_row(base_row_y, field_width, game_window, start_x)
        return success
    
    def start_cultivating_multi_row(self, base_row_y, field_width, game_window, start_x=0, fertilizer_data=None, num_rows=1):
        """Start cultivating multiple rows"""
        # Clear any previous active rows to prevent carryover from previous operations
        self.tractor.active_rows = []
        
        if num_rows == 1:
            return self.operations.start_cultivating_row(base_row_y, field_width, game_window, start_x, fertilizer_data)
        
        # For 3-row mode, cultivate the clicked row and one above/below if available and can be cultivated
        rows_to_cultivate = []
        
        # Add row above if available and can be cultivated
        if base_row_y - grid_size >= 0:
            if self.position_checker.can_cultivate_position(start_x, base_row_y - grid_size, game_window, fertilizer_data):
                rows_to_cultivate.append(base_row_y - grid_size)
        
        # Add the clicked row (base row)
        rows_to_cultivate.append(base_row_y)
        
        # Add row below if available, can be cultivated, and we need more rows
        if len(rows_to_cultivate) < num_rows and base_row_y + grid_size < game_window.height:
            if self.position_checker.can_cultivate_position(start_x, base_row_y + grid_size, game_window, fertilizer_data):
                rows_to_cultivate.append(base_row_y + grid_size)
        
        # Set up all rows to work on simultaneously
        self.tractor.active_rows = rows_to_cultivate
        if len(rows_to_cultivate) > 1:
            print(f"🚜 3-row cultivating: working on {len(rows_to_cultivate)} rows simultaneously")
        
        # Start with the base row (tractor sprite position)
        success = self.operations.start_cultivating_row(base_row_y, field_width, game_window, start_x, fertilizer_data)
        return success
    
    def start_cultivator_multi_row(self, base_row_y, field_width, game_window, start_x=0, num_rows=1):
        """Start removing weeds on multiple rows"""
        # Clear any previous active rows to prevent carryover from previous operations
        self.tractor.active_rows = []
        
        if num_rows == 1:
            return self.operations.start_cultivator_row(base_row_y, field_width, game_window, start_x)
        
        # For 3-row mode, work on the clicked row and one above/below if available and can be worked on
        rows_to_cultivate = []
        
        # Add row above if available and can be worked on
        if base_row_y - grid_size >= 0:
            if self.position_checker.can_cultivator_position(start_x, base_row_y - grid_size, game_window):
                rows_to_cultivate.append(base_row_y - grid_size)
        
        # Add the clicked row (base row)
        rows_to_cultivate.append(base_row_y)
        
        # Add row below if available, can be worked on, and we need more rows
        if len(rows_to_cultivate) < num_rows and base_row_y + grid_size < game_window.height:
            if self.position_checker.can_cultivator_position(start_x, base_row_y + grid_size, game_window):
                rows_to_cultivate.append(base_row_y + grid_size)
        
        # Set up all rows to work on simultaneously
        self.tractor.active_rows = rows_to_cultivate
        if len(rows_to_cultivate) > 1:
            print(f"🚜 3-row cultivator: working on {len(rows_to_cultivate)} rows simultaneously")
        
        # Start with the base row (tractor sprite position)
        success = self.operations.start_cultivator_row(base_row_y, field_width, game_window, start_x)
        return success

