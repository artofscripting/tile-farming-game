"""
Tractor Manager - Handles all tractor-related functionality
"""
import pyglet
from PIL import Image
from constants import tractor_batch, tractor_image, tractor_config, grid_size
from tractor import Tractor


class TractorManager:
    def __init__(self, game_window):
        self.game_window = game_window
        self.tractors = []
        self.active_tractor_index = 0
        self.tractor_cursor = None
        self.setup_initial_tractor()
    
    def get_tractor_speed(self):
        """Get the current tractor speed based on upgrades"""
        base_speed = 50
        is_speed_purchased = getattr(self.game_window.game_state, 'tractor_speed_purchased', False)
        if is_speed_purchased:
            return int(base_speed * 2.0)  # 200% of base speed (100% faster)
        return base_speed

    def setup_initial_tractor(self):
        """Set up the initial tractor"""
        speed = self.get_tractor_speed()
        first_tractor = Tractor(0, 0, speed)
        first_tractor.sprite.visible = False  # Hide tractor initially
        self.tractors = [first_tractor]  # Start with one tractor
        self.active_tractor_index = 0  # Currently selected tractor
        self.tractor_cursor = self.create_tractor_cursor()
    
    def create_tractor_cursor(self):
        """Create a custom cursor from the tractor image"""
        try:
            # Load the tractor image using PIL to convert to cursor format
            tractor_pil_image = Image.open('img/tractor.png')
            
            # Resize to tile size (24x24) to match game tiles
            cursor_size = (24, 24)
            tractor_pil_image = tractor_pil_image.resize(cursor_size, Image.Resampling.LANCZOS)
            
            # Ensure image has alpha channel
            if tractor_pil_image.mode != 'RGBA':
                tractor_pil_image = tractor_pil_image.convert('RGBA')
            
            # Convert PIL image to bytes (flip vertically for pyglet)
            tractor_pil_image = tractor_pil_image.transpose(Image.FLIP_TOP_BOTTOM)
            image_data = tractor_pil_image.tobytes()
            
            # Create pyglet ImageData
            image = pyglet.image.ImageData(
                cursor_size[0], cursor_size[1], 
                'RGBA', image_data,
                pitch=cursor_size[0] * 4  # Positive pitch after flip
            )
            
            # Create cursor with hotspot at center
            hotspot_x = cursor_size[0] // 2
            hotspot_y = cursor_size[1] // 2
            
            # Create cursor using pyglet's image cursor creation
            cursor = pyglet.window.ImageMouseCursor(image, hotspot_x, hotspot_y)
            
            print("Successfully created tractor cursor from img/tractor.png (24x24)")
            return cursor
            
        except Exception as e:
            print(f"Could not create tractor cursor: {e}")
            # Fallback to crosshair cursor
            return pyglet.window.Window.CURSOR_CROSSHAIR
    
    def get_active_tractor(self):
        """Get the currently active/selected tractor"""
        if self.tractors and 0 <= self.active_tractor_index < len(self.tractors):
            return self.tractors[self.active_tractor_index]
        return None
    
    def get_available_tractor(self):
        """Get an available (idle) tractor for a task"""
        for tractor in self.tractors:
            if tractor.is_idle():
                return tractor
        return None
    
    def purchase_tractor(self):
        """Purchase a new tractor using prestige points"""
        # Calculate cost: first tractor costs 30 prestige, each additional costs 20 more
        prestige_cost = 30 + (len(self.tractors) * 20)
        
        # Check if player has enough prestige
        current_prestige = getattr(self.game_window.game_state, 'prestige', 0)
        if current_prestige >= prestige_cost:
            # Deduct prestige
            self.game_window.game_state.prestige -= prestige_cost
            
            # Create new tractor at origin with unique position and current speed
            speed = self.get_tractor_speed()
            new_tractor = Tractor(0, len(self.tractors) * grid_size, speed)  # Offset by index
            self.tractors.append(new_tractor)
            
            # Auto-select the new tractor
            self.active_tractor_index = len(self.tractors) - 1
            self.update_tractor_highlighting()
            
            print(f"Purchased new tractor for {prestige_cost} prestige! Total tractors: {len(self.tractors)}")
            return True
        else:
            print(f"Cannot afford tractor ({prestige_cost} prestige needed, have {current_prestige})")
            return False
    
    def update_tractor_highlighting(self):
        """Update tractor highlighting to show which one is active (only when working)"""
        for i, tractor in enumerate(self.tractors):
            # Only show tractors when they are actually working or moving
            if tractor.moving:
                tractor.sprite.visible = True
            else:
                tractor.sprite.visible = False
    
    def select_next_tractor(self):
        """Select the next tractor in the list"""
        if len(self.tractors) > 1:
            self.active_tractor_index = (self.active_tractor_index + 1) % len(self.tractors)
            self.update_tractor_highlighting()
            print(f"Selected tractor {self.active_tractor_index + 1} of {len(self.tractors)}")
    
    def select_previous_tractor(self):
        """Select the previous tractor in the list"""
        if len(self.tractors) > 1:
            self.active_tractor_index = (self.active_tractor_index - 1) % len(self.tractors)
            self.update_tractor_highlighting()
            print(f"Selected tractor {self.active_tractor_index + 1} of {len(self.tractors)}")
    
    def rebuild_tractor_batch(self):
        """Rebuild the tractor batch if it becomes corrupted"""
        import constants
        
        # Clear the existing batch by creating a new one
        constants.tractor_batch = pyglet.graphics.Batch()
        
        # Recreate all tractor sprites in the new batch
        for tractor in self.tractors:
            if hasattr(tractor, 'sprite') and tractor.sprite:
                old_x, old_y = tractor.sprite.x, tractor.sprite.y
                old_visible = tractor.sprite.visible
                # Create new sprite in the new batch
                tractor.sprite = pyglet.sprite.Sprite(
                    tractor_image, 
                    x=old_x, 
                    y=old_y, 
                    batch=constants.tractor_batch
                )
                tractor.sprite.visible = old_visible
        
        print("Tractor batch rebuilt successfully")

