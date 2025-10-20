import pyglet
from pyglet import shapes
from constants import (
    OVERLAY_NONE, OVERLAY_WEEDS, OVERLAY_WATER, OVERLAY_NITROGEN, 
    OVERLAY_PHOSPHORUS, OVERLAY_POTASSIUM, OVERLAY_CALCIUM, 
    OVERLAY_MAGNESIUM, OVERLAY_SULFUR, OVERLAY_SEED_REQUIREMENTS, grid_size, 
    TILE_OWNED, TILE_TILLED, TILE_PLANTED, TILE_READY_HARVEST, seeds_config
)


class OverlayManager:
    def __init__(self, game_window):
        self.game_window = game_window
        self.current_overlay = OVERLAY_NONE
        self.selected_seed = None  # For seed requirements overlay
        self.overlay_shapes = []
        self.overlay_batch = pyglet.graphics.Batch()
        self.overlay_group = pyglet.graphics.Group(order=2)  # Draw overlays on top
        
    def set_overlay(self, overlay_type):
        """Set the current overlay type and update display"""
        self.current_overlay = overlay_type
        self.update_overlay_display()
    
    def set_seed_for_requirements(self, seed_name):
        """Set the selected seed for requirements overlay"""
        self.selected_seed = seed_name
        if self.current_overlay == OVERLAY_SEED_REQUIREMENTS:
            self.update_overlay_display()
        
    def get_overlay_name(self, overlay_type):
        """Get human-readable name for overlay type"""
        overlay_names = {
            OVERLAY_NONE: "None",
            OVERLAY_WEEDS: "Weeds",
            OVERLAY_WATER: "Water",
            OVERLAY_NITROGEN: "Nitrogen",
            OVERLAY_PHOSPHORUS: "Phosphorus", 
            OVERLAY_POTASSIUM: "Potassium",
            OVERLAY_CALCIUM: "Calcium",
            OVERLAY_MAGNESIUM: "Magnesium",
            OVERLAY_SULFUR: "Sulfur",
            OVERLAY_SEED_REQUIREMENTS: "Seed Requirements"
        }
        return overlay_names.get(overlay_type, "Unknown")
    
    def get_tile_overlay_value(self, tile, overlay_type):
        """Get the overlay value for a specific tile"""
        if overlay_type == OVERLAY_WEEDS:
            return getattr(tile, 'weeds', 0)
        elif overlay_type == OVERLAY_WATER:
            return tile.nutrients.get('water', 0)
        elif overlay_type == OVERLAY_NITROGEN:
            return tile.nutrients.get('nitrogen', 0)
        elif overlay_type == OVERLAY_PHOSPHORUS:
            return tile.nutrients.get('phosphorus', 0)
        elif overlay_type == OVERLAY_POTASSIUM:
            return tile.nutrients.get('potassium', 0)
        elif overlay_type == OVERLAY_CALCIUM:
            return tile.nutrients.get('calcium', 0)
        elif overlay_type == OVERLAY_MAGNESIUM:
            return tile.nutrients.get('magnesium', 0)
        elif overlay_type == OVERLAY_SULFUR:
            return tile.nutrients.get('sulfur', 0)
        elif overlay_type == OVERLAY_SEED_REQUIREMENTS:
            return self.check_seed_requirements(tile)
        return 0
    
    def check_seed_requirements(self, tile):
        """Check if tile meets double harvest requirements for selected seed"""
        if not self.selected_seed:
            return 0  # No seed selected
            
        # Find the seed configuration
        seed_config = None
        for seed in seeds_config:
            if seed['name'] == self.selected_seed:
                seed_config = seed
                break
                
        if not seed_config:
            return 0  # Seed not found
            
        # Check all nutrient requirements
        requirements = [
            ('water', seed_config.get('water_double', 0)),
            ('nitrogen', seed_config.get('nitrogen_double', 0)),
            ('phosphorus', seed_config.get('phosphorus_double', 0)),
            ('potassium', seed_config.get('potassium_double', 0)),
            ('calcium', seed_config.get('calcium_double', 0)),
            ('magnesium', seed_config.get('magnesium_double', 0)),
            ('sulfur', seed_config.get('sulfur_double', 0))
        ]
        
        # Check if all requirements are met
        for nutrient, required_amount in requirements:
            current_amount = tile.nutrients.get(nutrient, 0)
            if current_amount < required_amount:
                return 0  # Requirements not met (red)
                
        return 100  # All requirements met (green)
    
    def value_to_color(self, value, overlay_type):
        """Convert a value to a color gradient based on overlay type"""
        if overlay_type == OVERLAY_WEEDS:
            # For weeds: green (good) at low values, red (bad) at high values
            if value <= 0:
                return (0, 255, 0, 128)  # Green for no weeds (good)
            elif value >= 100:
                return (255, 0, 0, 128)  # Red for lots of weeds (bad)
            else:
                # Create gradient from green (0) to red (100)
                ratio = value / 100.0
                red = int(255 * ratio)        # 0 at 0, 255 at 100
                green = int(255 * (1 - ratio)) # 255 at 0, 0 at 100
                blue = 0
                return (red, green, blue, 128)
        elif overlay_type == OVERLAY_SEED_REQUIREMENTS:
            # For seed requirements: red (requirements not met), green (requirements met)
            if value <= 0:
                return (255, 0, 0, 128)  # Red - requirements not met
            else:
                return (0, 255, 0, 128)  # Green - requirements met
        else:
            # For nutrients/water: red (bad) at low values, green (good) at high values
            if value <= 0:
                return (255, 0, 0, 128)  # Solid red with transparency
            elif value >= 100:
                return (0, 255, 0, 128)  # Solid green with transparency
            else:
                # Create smooth gradient from red (0) to green (100)
                ratio = value / 100.0
                red = int(255 * (1 - ratio))  # 255 at 0, 0 at 100
                green = int(255 * ratio)      # 0 at 0, 255 at 100
                blue = 0                      # Always 0 for red-green gradient
                return (red, green, blue, 128)  # With transparency
    
    def update_overlay_display(self):
        """Update the overlay display based on current overlay type"""
        # Clear existing overlay shapes
        for shape in self.overlay_shapes:
            shape.delete()
        self.overlay_shapes.clear()
        
        if self.current_overlay == OVERLAY_NONE:
            return
            
        # Create overlay shapes for each relevant tile
        for tile in self.game_window.farm_tiles:
            # Only show overlays on farmed tiles
            if tile.state in [TILE_OWNED, TILE_TILLED, TILE_PLANTED, TILE_READY_HARVEST]:
                value = self.get_tile_overlay_value(tile, self.current_overlay)
                color = self.value_to_color(value, self.current_overlay)
                
                # Create a semi-transparent rectangle overlay
                overlay_rect = shapes.Rectangle(
                    tile.x, tile.y, grid_size, grid_size,
                    color=color[:3],  # RGB without alpha
                    batch=self.overlay_batch,
                    group=self.overlay_group
                )
                overlay_rect.opacity = color[3]  # Set alpha
                self.overlay_shapes.append(overlay_rect)
    
    def draw(self):
        """Draw the overlay and update it every frame"""
        if self.current_overlay != OVERLAY_NONE:
            # Update overlay display every frame to reflect real-time changes
            self.update_overlay_display()
            self.overlay_batch.draw()
    
    def clear(self):
        """Clear all overlays"""
        self.set_overlay(OVERLAY_NONE)

