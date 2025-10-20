from constants import (
    grid_size, TILE_OWNED, TILE_TILLED, TILE_UNOWNED, TILE_READY_HARVEST, 
    TILE_BARN, TILE_SEED_BIN, TILE_GROWING
)
from tractor_position import TractorPositionChecker


class TractorOperations:
    """Handles single-row tractor operations"""
    
    def __init__(self, tractor_core):
        self.tractor = tractor_core
        self.position_checker = TractorPositionChecker()
    
    def start_tilling_row(self, row_y, field_width, game_window, start_x=0):
        """Start tilling a specific row from a specific starting position"""
        self.tractor.target_y = row_y
        self.tractor.sprite.y = row_y
        
        # Check if starting position is owned
        if not self.position_checker.can_start_tilling(start_x, row_y, game_window):
            print("Cannot start tractor on unowned tile!")
            return False
        
        # Start at the specified position and move right
        self.tractor.sprite.x = start_x
        self.tractor.target_x = field_width - grid_size
        self.tractor.row_direction = 1  # Always move left to right
        self.tractor.mode = 'till'  # Ensure we're in tilling mode
        
        # Show tractor when it starts working
        self.tractor.show()
            
        # Till the starting position
        self.till_current_position(game_window)
        self.tractor.moving = True
        return True
    
    def start_planting_row(self, row_y, field_width, game_window, start_x=0, seed_type=None):
        """Start planting seeds in a specific row from a specific starting position"""
        self.tractor.target_y = row_y
        self.tractor.sprite.y = row_y
        
        # Check if starting position is tilled and we have seeds
        if not self.position_checker.can_start_planting_position(start_x, row_y, game_window, seed_type):
            print(f"Cannot start planting: tile not tilled or no {seed_type} seeds available!")
            return False
        
        # Start at the specified position and move right
        self.tractor.sprite.x = start_x
        self.tractor.target_x = field_width - grid_size
        self.tractor.row_direction = 1  # Always move left to right
        self.tractor.mode = 'plant'
        self.tractor.selected_seed = seed_type
        
        # Show tractor when it starts working
        self.tractor.show()
            
        # Plant at the starting position
        self.plant_current_position(game_window)
        self.tractor.moving = True
        return True
    
    def start_harvesting_row(self, row_y, field_width, game_window, start_x=0):
        """Start harvesting crops in a specific row from a specific starting position"""
        self.tractor.target_y = row_y
        self.tractor.sprite.y = row_y
        
        # Check if starting position has harvestable crops
        if not self.position_checker.can_start_harvesting_position(start_x, row_y, game_window):
            print("Cannot start harvesting: no harvestable crops in this row!")
            return False
        
        # Start at the specified position and move right
        self.tractor.sprite.x = start_x
        self.tractor.target_x = field_width - grid_size
        self.tractor.row_direction = 1  # Always move left to right
        self.tractor.mode = 'harvest'
        
        # Show tractor when it starts working
        self.tractor.show()
            
        # Harvest at the starting position
        self.harvest_current_position(game_window)
        self.tractor.moving = True
        return True
    
    def start_cultivating_row(self, row_y, field_width, game_window, start_x=0, fertilizer_data=None):
        """Start applying fertilizer in a specific row from a specific starting position"""
        if not fertilizer_data:
            print("No fertilizer selected for cultivation!")
            return False
            
        self.tractor.target_y = row_y
        self.tractor.sprite.y = row_y
        
        # Check if starting position can be cultivated
        if not self.position_checker.can_cultivate_position(start_x, row_y, game_window, fertilizer_data):
            print(f"Cannot start cultivating: tile not suitable or cannot afford {fertilizer_data['name']} (${fertilizer_data['cost']})!")
            return False
        
        # Start at the specified position and move right
        self.tractor.sprite.x = start_x
        self.tractor.target_x = field_width - grid_size
        self.tractor.row_direction = 1  # Always move left to right
        self.tractor.mode = 'cultivate'
        self.tractor.selected_fertilizer = fertilizer_data
        
        # Clear the cultivated tiles tracking for new operation
        self.tractor.cultivated_tiles = set()
        
        # Show tractor when it starts working
        self.tractor.show()
        self.tractor.moving = True  
        return True
    
    def start_cultivator_row(self, row_y, field_width, game_window, start_x=0):
        """Start removing weeds in a specific row from a specific starting position"""
        self.tractor.target_y = row_y
        self.tractor.sprite.y = row_y
        
        # Check if starting position can be worked on (any farmed tile state)
        if not self.position_checker.can_cultivator_position(start_x, row_y, game_window):
            print("Cannot start cultivator: tile not suitable for weed removal!")
            return False
        
        # Start at the specified position and move right
        self.tractor.sprite.x = start_x
        self.tractor.target_x = field_width - grid_size
        self.tractor.row_direction = 1  # Always move left to right
        self.tractor.mode = 'cultivator'
        
        # Clear the cultivated tiles tracking for new operation (reuse for weed tracking)
        self.tractor.cultivated_tiles = set()
        
        # Show tractor when it starts working
        self.tractor.show()
        self.tractor.moving = True  
        return True
    
    def till_current_position(self, game_window):
        """Convert the tile under the tractor to tilled soil (only works on owned tiles)"""
        tile = self.tractor.get_tile_at_position(self.tractor.sprite.x, self.tractor.sprite.y, game_window)
        
        if tile:
            # Only till owned tiles (convert owned to tilled)
            if tile.state == TILE_OWNED:
                tile.set_state(TILE_TILLED)
            # If it's already tilled, do nothing
            # If it's unowned, the tractor shouldn't be here (safety check)
            elif tile.state == TILE_UNOWNED:
                print("Warning: Tractor on unowned tile!")
                self.tractor.process_job_completion(game_window)
                self.tractor.moving = False
                # Hide tractor when it encounters problems
                self.tractor.hide()
    
    def plant_current_position(self, game_window):
        """Plant seeds at the current tractor position"""
        tile = self.tractor.get_tile_at_position(self.tractor.sprite.x, self.tractor.sprite.y, game_window)
        
        if tile and tile.state == TILE_TILLED and self.tractor.selected_seed:
            # Find a seed bin with the selected seed type
            seed_bin = None
            for bin_tile in game_window.farm_tiles:
                if (bin_tile.state == TILE_SEED_BIN and 
                    bin_tile.stored_crop_type == self.tractor.selected_seed and 
                    bin_tile.stored_amount > 0):
                    seed_bin = bin_tile
                    break
            
            if seed_bin:
                # Use one seed from the bin
                seed_bin.stored_amount -= 1
                # Seeds are already paid for when purchased, no additional cost for planting
                tile.plant_crop(self.tractor.selected_seed)
            else:
                # No more seeds, stop the tractor
                print(f"Out of {self.tractor.selected_seed} seeds in seed bins!")
                self.tractor.process_job_completion(game_window)
                self.tractor.moving = False
                self.tractor.hide()
    
    def harvest_current_position(self, game_window):
        """Harvest crops at the current tractor position"""
        tile = self.tractor.get_tile_at_position(self.tractor.sprite.x, self.tractor.sprite.y, game_window)
        
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
    
    def cultivate_current_position(self, game_window):
        """Apply fertilizer at the current tractor position (only once per tile)"""
        if not hasattr(self.tractor, 'selected_fertilizer') or not self.tractor.selected_fertilizer:
            return
            
        tile = self.tractor.get_tile_at_position(self.tractor.sprite.x, self.tractor.sprite.y, game_window)
        
        if tile:
            # Create unique identifier for this tile position
            tile_id = (int(tile.x // grid_size), int(tile.y // grid_size))
            
            # Only process if we haven't cultivated this tile yet
            if tile_id not in self.tractor.cultivated_tiles and self.position_checker.can_cultivate_position(self.tractor.sprite.x, self.tractor.sprite.y, game_window, self.tractor.selected_fertilizer):
                # Mark this tile as cultivated
                self.tractor.cultivated_tiles.add(tile_id)
                
                # Apply fertilizer nutrients to the tile
                fertilizer = self.tractor.selected_fertilizer
                
                # Add to fertilizer cost accumulator (payment will be processed at job completion)
                self.tractor.add_to_fertilizer_accumulator(fertilizer['name'], fertilizer['cost'])
                
                # Apply nutrients from fertilizer to tile
                nutrient_keys = ['nitrogen', 'phosphorus', 'potassium', 'calcium', 'magnesium', 'sulfur', 'water']
                nutrients_added = []
                
                for nutrient in nutrient_keys:
                    if nutrient in fertilizer and hasattr(tile, 'nutrients') and nutrient in tile.nutrients:
                        amount = fertilizer[nutrient]
                        if amount > 0:  # Only add if amount is positive
                            tile.nutrients[nutrient] += amount
                            nutrients_added.append(f"{nutrient}+{amount}")
                
                # Update visual appearance based on new nutrient levels
                tile.update_visual_appearance()
                        
                print(f"Applied {fertilizer['name']} fertilizer to tile at ({int(tile.x)}, {int(tile.y)}) - will be charged ${fertilizer['cost']} at job completion")
                
                # Log nutrient increases
                if nutrients_added:
                    nutrient_summary = ", ".join(nutrients_added)
                    print(f"  Nutrients added: {nutrient_summary}")
                else:
                    print(f"  No nutrients added (fertilizer contains no positive nutrient values)")
    
    def cultivate_weeds_current_position(self, game_window):
        """Remove weeds at the current tractor position (only once per tile)"""
        tile = self.tractor.get_tile_at_position(self.tractor.sprite.x, self.tractor.sprite.y, game_window)
        
        if tile:
            # Create unique identifier for this tile position
            tile_id = (int(tile.x // grid_size), int(tile.y // grid_size))
            
            # Only process if we haven't worked on this tile yet and it's a farmed tile
            if tile_id not in self.tractor.cultivated_tiles and self.position_checker.can_cultivator_position(self.tractor.sprite.x, self.tractor.sprite.y, game_window):
                # Mark this tile as worked on
                self.tractor.cultivated_tiles.add(tile_id)
                
                # Remove weeds (works even if weeds are already 0)
                if tile.cultivate_weeds():
                    print(f"🚜 Tractor removed weeds at ({tile.x}, {tile.y})")
                else:
                    # Still processed the tile, just no weeds to remove
                    print(f"🚜 Tractor processed tile at ({tile.x}, {tile.y}) - no weeds found")

