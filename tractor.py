from tractor_core import TractorCore
from tractor_operations import TractorOperations
from tractor_multi_row import TractorMultiRow
from tractor_position import TractorPositionChecker


class Tractor:
    """Main Tractor class that coordinates all tractor functionality"""
    
    def __init__(self, x, y, speed=50):
        # Initialize core tractor functionality
        self.core = TractorCore(x, y, speed)
        
        # Initialize operation handlers
        self.operations = TractorOperations(self.core)
        self.multi_row = TractorMultiRow(self.core)
        self.position_checker = TractorPositionChecker()
        
        # Expose commonly used core attributes for backward compatibility
        self.sprite = self.core.sprite
        self.speed = self.core.speed
        self.moving = self.core.moving
        self.mode = self.core.mode
        self.selected_seed = self.core.selected_seed
        self.selected_fertilizer = self.core.selected_fertilizer
        self.active_rows = self.core.active_rows
    
    @property
    def x(self):
        """Get the tractor's x position"""
        return self.core.sprite.x
    
    @x.setter
    def x(self, value):
        """Set the tractor's x position"""
        self.core.sprite.x = value
        self.core.target_x = value
    
    @property 
    def y(self):
        """Get the tractor's y position"""
        return self.core.sprite.y
    
    @y.setter
    def y(self, value):
        """Set the tractor's y position"""
        self.core.sprite.y = value
        self.core.target_y = value
    
    def is_idle(self):
        """Check if the tractor is idle (not moving)"""
        return self.core.is_idle()
        
    def get_tile_at_position(self, x, y, game_window):
        """Get the tile at the specified position"""
        return self.core.get_tile_at_position(x, y, game_window)
    
    def can_start_tilling(self, x, y, game_window):
        """Check if the tractor can start tilling at a specific position"""
        return self.position_checker.can_start_tilling(x, y, game_window)
    
    def can_till_position(self, x, y, game_window):
        """Check if there are tillable tiles ahead (for continuation logic)"""
        return self.position_checker.can_till_position(x, y, game_window)
    
    def can_harvest_position(self, x, y, game_window):
        """Check if the tractor can continue harvesting"""
        return self.position_checker.can_harvest_position(x, y, game_window)
    
    def has_harvestable_crops_in_row(self, row_y, game_window, start_x=0):
        """Check if a row has any harvestable crops starting from a specific position"""
        return self.position_checker.has_harvestable_crops_in_row(row_y, game_window, start_x)
        
    def start_tilling_row(self, row_y, field_width, game_window, start_x=0):
        """Start tilling a specific row from a specific starting position"""
        return self.operations.start_tilling_row(row_y, field_width, game_window, start_x)
    
    def start_planting_row(self, row_y, field_width, game_window, start_x=0, seed_type=None):
        """Start planting seeds in a specific row from a specific starting position"""
        return self.operations.start_planting_row(row_y, field_width, game_window, start_x, seed_type)
    
    def start_harvesting_row(self, row_y, field_width, game_window, start_x=0):
        """Start harvesting crops in a specific row from a specific starting position"""
        return self.operations.start_harvesting_row(row_y, field_width, game_window, start_x)
    
    def start_cultivating_row(self, row_y, field_width, game_window, start_x=0, fertilizer_data=None):
        """Start cultivating a specific row from a specific starting position"""
        return self.operations.start_cultivating_row(row_y, field_width, game_window, start_x, fertilizer_data)
        
    def update(self, dt, game_window):
        """Update tractor movement and operations"""
        if not self.core.moving:
            return
            
        # Move towards target (always moving right)
        if self.core.sprite.x < self.core.target_x:
            # Move to next position
            self.core.sprite.x += self.core.speed * dt
            
            # Sync attributes for backward compatibility
            self.moving = self.core.moving
            self.mode = self.core.mode
            self.selected_seed = self.core.selected_seed
            self.selected_fertilizer = self.core.selected_fertilizer
            
            # Perform action at current position on all active rows
            if self.core.mode == 'till':
                self.multi_row.till_current_position_multi_row(game_window)
            elif self.core.mode == 'plant':
                self.multi_row.plant_current_position_multi_row(game_window)
            elif self.core.mode == 'harvest':
                self.multi_row.harvest_current_position_multi_row(game_window)
            elif self.core.mode == 'cultivate':
                self.multi_row.cultivate_current_position_multi_row(game_window)
            elif self.core.mode == 'cultivator':
                self.multi_row.cultivate_weeds_current_position_multi_row(game_window)
                
            # Check if we should continue based on current mode
            if self.core.mode == 'till':
                if not self.position_checker.can_till_position(self.core.sprite.x, self.core.sprite.y, game_window):
                    print("Tractor stopped: no more tiles to till")
                    self.core.process_job_completion(game_window)
                    self.core.moving = False
                    self.core.hide()
                    return
            elif self.core.mode == 'plant':
                if not self.position_checker.can_plant_position(self.core.sprite.x, self.core.sprite.y, game_window, self.core.selected_seed):
                    print("Tractor stopped: no more seeds or untilled ground")
                    self.core.process_job_completion(game_window)
                    self.core.moving = False
                    self.core.hide()
                    return
            elif self.core.mode == 'harvest':
                if not self.position_checker.can_harvest_position(self.core.sprite.x, self.core.sprite.y, game_window):
                    print("Tractor stopped: no more crops to harvest")
                    self.core.process_job_completion(game_window)
                    self.core.moving = False
                    self.core.hide()
                    return
            elif self.core.mode == 'cultivate':
                if not hasattr(self.core, 'selected_fertilizer') or not self.core.selected_fertilizer:
                    print("Tractor stopped: no fertilizer selected")
                    self.core.process_job_completion(game_window)
                    self.core.moving = False
                    self.core.hide()
                    return
                if not self.position_checker.can_cultivate_position(self.core.sprite.x, self.core.sprite.y, game_window, self.core.selected_fertilizer):
                    print("Tractor stopped: no more tiles to cultivate or cannot afford fertilizer")
                    self.core.process_job_completion(game_window)
                    self.core.moving = False
                    self.core.hide()
                    return
            elif self.core.mode == 'cultivator':
                # Check if there are more cultivatable tiles ahead or if we hit an unowned tile
                if not self.position_checker.can_cultivator_continue(self.core.sprite.x, self.core.sprite.y, game_window):
                    print("Tractor stopped: reached end of cultivatable area")
                    self.core.process_job_completion(game_window)
                    self.core.moving = False
                    self.core.hide()
                    return
        else:
            # Reached the end, process final position on all active rows and stop
            if self.core.mode == 'till':
                self.multi_row.till_current_position_multi_row(game_window)
            elif self.core.mode == 'plant':
                self.multi_row.plant_current_position_multi_row(game_window)
            elif self.core.mode == 'harvest':
                self.multi_row.harvest_current_position_multi_row(game_window)
            elif self.core.mode == 'cultivate':
                self.multi_row.cultivate_current_position_multi_row(game_window)
            elif self.core.mode == 'cultivator':
                self.multi_row.cultivate_weeds_current_position_multi_row(game_window)

            # Process any accumulated job transactions before resetting state
            self.core.process_job_completion(game_window)
            self.core.reset_state()
            # Sync attributes for backward compatibility
            self.moving = self.core.moving
            self.mode = self.core.mode
            self.selected_seed = self.core.selected_seed
            self.selected_fertilizer = self.core.selected_fertilizer
    
    def can_plant_position(self, x, y, game_window, seed_type):
        """Check if the tractor can continue planting"""
        return self.position_checker.can_plant_position(x, y, game_window, seed_type)
    
    def can_cultivate_position(self, x, y, game_window, fertilizer_data):
        """Check if the tractor can apply fertilizer at the current position"""
        return self.position_checker.can_cultivate_position(x, y, game_window, fertilizer_data)
    
    # Multi-row operation methods (delegate to multi_row handler)
    def start_tilling_multi_row(self, base_row_y, field_width, game_window, start_x=0, num_rows=1):
        """Start tilling multiple rows"""
        result = self.multi_row.start_tilling_multi_row(base_row_y, field_width, game_window, start_x, num_rows)
        # Sync attributes for backward compatibility
        self.moving = self.core.moving
        self.mode = self.core.mode
        self.active_rows = self.core.active_rows
        return result
    
    def start_planting_multi_row(self, base_row_y, field_width, game_window, start_x=0, seed_type=None, num_rows=1):
        """Start planting multiple rows"""
        result = self.multi_row.start_planting_multi_row(base_row_y, field_width, game_window, start_x, seed_type, num_rows)
        # Sync attributes for backward compatibility
        self.moving = self.core.moving
        self.mode = self.core.mode
        self.selected_seed = self.core.selected_seed
        self.active_rows = self.core.active_rows
        return result
    
    def start_harvesting_multi_row(self, base_row_y, field_width, game_window, start_x=0, num_rows=1):
        """Start harvesting multiple rows"""
        result = self.multi_row.start_harvesting_multi_row(base_row_y, field_width, game_window, start_x, num_rows)
        # Sync attributes for backward compatibility
        self.moving = self.core.moving
        self.mode = self.core.mode
        self.active_rows = self.core.active_rows
        return result
    
    def start_cultivating_multi_row(self, base_row_y, field_width, game_window, start_x=0, fertilizer_data=None, num_rows=1):
        """Start cultivating multiple rows"""
        result = self.multi_row.start_cultivating_multi_row(base_row_y, field_width, game_window, start_x, fertilizer_data, num_rows)
        # Sync attributes for backward compatibility
        self.moving = self.core.moving
        self.mode = self.core.mode
        self.selected_fertilizer = self.core.selected_fertilizer
        self.active_rows = self.core.active_rows
        return result
    
    def start_cultivator_multi_row(self, base_row_y, field_width, game_window, start_x=0, num_rows=1):
        """Start removing weeds on multiple rows"""
        result = self.multi_row.start_cultivator_multi_row(base_row_y, field_width, game_window, start_x, num_rows)
        # Sync attributes for backward compatibility
        self.moving = self.core.moving
        self.mode = self.core.mode
        self.active_rows = self.core.active_rows
        return result

