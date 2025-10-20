import pyglet
from constants import (
    tractor_image, tractor_batch, grid_size, 
    TILE_OWNED, TILE_TILLED, TILE_UNOWNED, TILE_READY_HARVEST, TILE_BARN
)


class TractorCore:
    """Core tractor functionality and sprite management"""
    
    def __init__(self, x, y, speed=50):
        self.sprite = pyglet.sprite.Sprite(tractor_image, x=x, y=y, batch=tractor_batch)
        # Scale the tractor to fit the grid size
        self.sprite.scale_x = grid_size / self.sprite.width
        self.sprite.scale_y = grid_size / self.sprite.height
        # Hide tractor initially
        self.sprite.visible = False
        self.speed = speed
        self.target_x = x
        self.target_y = y
        self.moving = False
        self.row_direction = 1  # 1 for right, -1 for left
        self.mode = 'till'  # 'till', 'plant', 'harvest', or 'cultivate'
        self.selected_seed = None
        self.selected_fertilizer = None
        self.cultivated_tiles = set()  # Track tiles that have been cultivated in current operation
        
        # Multi-row operation variables
        self.additional_rows = []
        self.current_operation = None
        self.field_width = 0
        self.start_x = 0
        self.current_seed_type = None
        self.current_fertilizer_data = None
        self.active_rows = []  # List of rows to work on simultaneously
        
        # Job transaction accumulators for end-of-job processing
        self.job_harvest_accumulator = {}  # {crop_type: {'sold': amount, 'stored': amount, 'total_value': value}}
        self.job_fertilizer_accumulator = {}  # {fertilizer_name: {'tiles_applied': count, 'cost_per_tile': cost, 'total_cost': cost}}
    
    def is_idle(self):
        """Check if the tractor is idle (not moving)"""
        return not self.moving
        
    def get_tile_at_position(self, x, y, game_window):
        """Get the tile at the specified position"""
        grid_x = int(x // grid_size) * grid_size
        grid_y = int(y // grid_size) * grid_size
        
        for tile in game_window.farm_tiles:
            if (abs(tile.x - grid_x) < grid_size/2 and 
                abs(tile.y - grid_y) < grid_size/2):
                return tile
        return None
    
    def show(self):
        """Show the tractor sprite"""
        self.sprite.visible = True
    
    def hide(self):
        """Hide the tractor sprite"""
        self.sprite.visible = False
    
    def add_to_harvest_accumulator(self, crop_type, amount, was_stored, market_price):
        """Add harvested crop to the job accumulator"""
        if crop_type not in self.job_harvest_accumulator:
            self.job_harvest_accumulator[crop_type] = {'sold': 0, 'stored': 0, 'total_value': 0}
        
        if was_stored:
            self.job_harvest_accumulator[crop_type]['stored'] += amount
        else:
            self.job_harvest_accumulator[crop_type]['sold'] += amount
            self.job_harvest_accumulator[crop_type]['total_value'] += market_price * amount
    
    def add_to_fertilizer_accumulator(self, fertilizer_name, cost):
        """Add fertilizer application to the job accumulator"""
        if fertilizer_name not in self.job_fertilizer_accumulator:
            self.job_fertilizer_accumulator[fertilizer_name] = {'tiles_applied': 0, 'cost_per_tile': cost, 'total_cost': 0}
        
        self.job_fertilizer_accumulator[fertilizer_name]['tiles_applied'] += 1
        self.job_fertilizer_accumulator[fertilizer_name]['total_cost'] += cost
    
    def process_job_harvest_sales(self, game_window):
        """Process all accumulated harvest sales as a single transaction at job completion"""
        if not self.job_harvest_accumulator:
            return
        
        total_value = 0
        crop_details = []
        
        for crop_type, data in self.job_harvest_accumulator.items():
            if data['sold'] > 0:
                total_value += data['total_value']
                crop_details.append(f"{data['sold']} {crop_type}")
                
        if total_value > 0:
            crop_list = ", ".join(crop_details)
            game_window.game_state.earn_money(
                total_value,
                'crop_sale',
                f"Harvest job completed - sold {crop_list} for ${total_value:.2f}",
                {
                    'job_type': 'harvest',
                    'crops_sold': self.job_harvest_accumulator,
                    'total_value': total_value
                }
            )
            print(f"🚜 Job completed! Sold {crop_list} for ${total_value:.2f}")
        
        # Reset accumulator for next job
        self.job_harvest_accumulator = {}
    
    def process_job_fertilizer_costs(self, game_window):
        """Process all accumulated fertilizer costs as a single transaction at job completion"""
        if not self.job_fertilizer_accumulator:
            return
        
        total_cost = 0
        fertilizer_details = []
        
        for fertilizer_name, data in self.job_fertilizer_accumulator.items():
            total_cost += data['total_cost']
            fertilizer_details.append(f"{data['tiles_applied']} tiles with {fertilizer_name}")
            
        if total_cost > 0:
            fertilizer_list = ", ".join(fertilizer_details)
            success = game_window.game_state.spend_money(
                total_cost,
                'fertilizer_purchase',
                f"Fertilizing job completed - applied {fertilizer_list} for ${total_cost:.2f}",
                {
                    'job_type': 'fertilizing',
                    'fertilizers_used': self.job_fertilizer_accumulator,
                    'total_cost': total_cost
                }
            )
            
            if success:
                print(f"🚜 Job completed! Applied {fertilizer_list} for ${total_cost:.2f}")
            else:
                print(f"❌ Job failed! Could not afford ${total_cost:.2f} for fertilizer costs")
                # Return false to indicate the job failed due to insufficient funds
                return False
        
        # Reset accumulator for next job
        self.job_fertilizer_accumulator = {}
        return True
    
    def process_job_completion(self, game_window):
        """Process all accumulated transactions (harvest sales and fertilizer costs) at job completion"""
        # Process fertilizer costs first (spending money)
        fertilizer_success = self.process_job_fertilizer_costs(game_window)
        
        # Process harvest sales (earning money)
        self.process_job_harvest_sales(game_window)
        
        return fertilizer_success

    def reset_state(self):
        """Reset tractor to idle state"""
        self.moving = False
        self.hide()
        self.mode = 'till'
        self.cultivated_tiles = set()
        self.selected_seed = None
        self.additional_rows = []
        self.current_operation = None
        self.active_rows = []
        
        # Clear job accumulators 
        self.job_harvest_accumulator = {}
        self.job_fertilizer_accumulator = {}

