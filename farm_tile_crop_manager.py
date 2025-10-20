import pyglet
import time
from constants import (
    grid_size, crop_images, seeds_config, TILE_PLANTED, TILE_READY_HARVEST,
    ui_batch, TILE_OWNED, TILE_TILLED, BUILDING_BARN, BUILDING_SEED_BIN,
    TILE_BARN, TILE_SEED_BIN
)


class FarmTileCropManager:
    """Manages crop planting, growth, and harvesting for a farm tile"""

    def __init__(self, tile):
        self.tile = tile
        self.crop_type = None
        self.plant_time = None
        self.growth_time = 0
        self.crop_sprite = None
        self.original_crop_width = None
        self.original_crop_height = None
        self.current_scale = 0.5  # Current visual scale (0.5 to 1.0)

    def plant_crop(self, crop_name):
        """Plant a crop on the tile"""
        if self.tile.state == TILE_TILLED and crop_name in crop_images:
            self.crop_type = crop_name
            self.plant_time = time.time()

            # Create crop sprite using grow.png when planted
            if self.crop_sprite:
                self.crop_sprite.visible = False

            from constants import pyglet
            grow_image = pyglet.resource.image('img/grow.png')
            try:
                self.crop_sprite = pyglet.sprite.Sprite(grow_image, x=self.tile.x, y=self.tile.y, batch=ui_batch)
            except Exception as e:
                print(f"Error creating grow sprite: {e}")
                self.crop_sprite = pyglet.sprite.Sprite(grow_image, x=self.tile.x, y=self.tile.y)

            self.original_crop_width = self.crop_sprite.image.width
            self.original_crop_height = self.crop_sprite.image.height

            self.current_scale = 0.5
            half_scale_x = (grid_size * self.current_scale) / self.original_crop_width
            half_scale_y = (grid_size * self.current_scale) / self.original_crop_height
            self.crop_sprite.scale_x = half_scale_x
            self.crop_sprite.scale_y = half_scale_y
            self.crop_sprite.x = self.tile.x + grid_size * (1 - self.current_scale) / 2
            self.crop_sprite.y = self.tile.y + grid_size * (1 - self.current_scale) / 2
            self.crop_sprite.visible = True

            # Find growth time for this crop
            for seed in seeds_config:
                if seed['name'] == crop_name:
                    self.growth_time = seed['growth_time']
                    break

            self.tile.set_state(TILE_PLANTED)
            return True
        return False

    def update_growth(self):
        """Update crop growth progress"""
        if self.tile.state == TILE_PLANTED and self.plant_time:
            elapsed = (time.time() - self.plant_time) * 1000  # Convert to milliseconds
            if elapsed >= self.growth_time:
                self.tile.state = TILE_READY_HARVEST
                self.current_scale = 1.0
                print(f"🌱 {self.crop_type} crop is ready for harvest! (grew in {elapsed:.1f}ms)")
                # Switch to crop icon when ready for harvest
                from constants import crop_images
                if self.crop_type in crop_images:
                    try:
                        self.crop_sprite.image = crop_images[self.crop_type]
                        # Update original dimensions to new image
                        self.original_crop_width = self.crop_sprite.image.width
                        self.original_crop_height = self.crop_sprite.image.height
                    except Exception as e:
                        print(f"Error switching to crop icon for {self.crop_type}: {e}")
                # Scale crop to full size to fit the tile
                if self.crop_sprite and self.original_crop_width:
                    full_scale_x = grid_size / self.original_crop_width
                    full_scale_y = grid_size / self.original_crop_height
                    self.crop_sprite.scale_x = full_scale_x
                    self.crop_sprite.scale_y = full_scale_y
                    self.crop_sprite.x = self.tile.x
                    self.crop_sprite.y = self.tile.y
                    # Reset position to tile corner (full size)
                    self.crop_sprite.x = self.tile.x
                    self.crop_sprite.y = self.tile.y
            else:
                # Update visual growth progress
                growth_progress = elapsed / self.growth_time
                self.current_scale = 0.5 + (growth_progress * 0.5)  # Scale from 0.5 to 1.0
                
                if self.crop_sprite and self.original_crop_width:
                    scale_x = (grid_size * self.current_scale) / self.original_crop_width
                    scale_y = (grid_size * self.current_scale) / self.original_crop_height
                    self.crop_sprite.scale_x = scale_x
                    self.crop_sprite.scale_y = scale_y
                    # Center the sprite based on current scale
                    self.crop_sprite.x = self.tile.x + grid_size * (1 - self.current_scale) / 2
                    self.crop_sprite.y = self.tile.y + grid_size * (1 - self.current_scale) / 2

    def harvest(self, nutrient_manager):
        """Harvest the crop if ready"""
        if self.tile.state == TILE_READY_HARVEST and self.crop_type:
            # Base harvest amount is 1
            amount = 1

            # Find seed data for nutrient checks
            seed_data = None
            for seed in seeds_config:
                if seed['name'] == self.crop_type:
                    seed_data = seed
                    break

            # Check if nutrients meet doubling thresholds
            if seed_data and nutrient_manager.check_nutrient_doubling_bonus(seed_data):
                amount *= 2
                print(f"🌟 Nutrient bonus! {self.crop_type} harvest doubled to {amount} units!")

            # Consume nutrients based on crop requirements
            if seed_data:
                nutrient_manager.consume_nutrients_for_harvest(seed_data)

            # Clear crop
            crop_name = self.crop_type
            self.crop_type = None
            self.plant_time = None
            self.growth_time = 0
            if self.crop_sprite:
                self.crop_sprite.visible = False

            # Restore tile state: if there's a building, show it; otherwise owned
            if self.tile.building_manager.building_type == BUILDING_BARN:
                self.tile.set_state(TILE_BARN)
            elif self.tile.building_manager.building_type == BUILDING_SEED_BIN:
                self.tile.set_state(TILE_SEED_BIN)
            else:
                self.tile.set_state(TILE_OWNED)

            return crop_name, amount
        return None, 0

    def get_crop_type(self):
        """Get the current crop type"""
        return self.crop_type

    def has_crop_sprite(self):
        """Check if crop sprite exists"""
        return self.crop_sprite is not None

    def restore_crop_state(self, crop_type, growth_time, plant_time, tile_state, current_scale=None):
        """Restore crop state from saved data without resetting plant time"""
        if crop_type:
            self.crop_type = crop_type
            self.growth_time = growth_time
            self.plant_time = plant_time
            
            # Set current scale (default based on tile state if not provided)
            if current_scale is not None:
                self.current_scale = current_scale
            elif tile_state == TILE_READY_HARVEST:
                self.current_scale = 1.0
            else:
                self.current_scale = 0.5
            
            # Try to create crop sprite if image is available
            if crop_type in crop_images:
                if self.crop_sprite:
                    self.crop_sprite.visible = False
                
                # Choose the correct image based on tile state
                if tile_state == TILE_READY_HARVEST:
                    sprite_image = crop_images[crop_type]
                else:
                    # For planted/growing crops, use the grow.png image
                    from constants import pyglet
                    sprite_image = pyglet.resource.image('img/grow.png')
                
                try:
                    self.crop_sprite = pyglet.sprite.Sprite(sprite_image, x=self.tile.x, y=self.tile.y, batch=ui_batch)
                except Exception as e:
                    print(f"Error creating crop sprite for {crop_type}: {e}")
                    self.crop_sprite = pyglet.sprite.Sprite(sprite_image, x=self.tile.x, y=self.tile.y)
                
                # Store original image dimensions for proper scaling
                self.original_crop_width = self.crop_sprite.image.width
                self.original_crop_height = self.crop_sprite.image.height
                
                # Set sprite size and position based on current scale
                if self.original_crop_width:
                    scale_x = (grid_size * self.current_scale) / self.original_crop_width
                    scale_y = (grid_size * self.current_scale) / self.original_crop_height
                    self.crop_sprite.scale_x = scale_x
                    self.crop_sprite.scale_y = scale_y
                    # Center the sprite based on current scale
                    self.crop_sprite.x = self.tile.x + grid_size * (1 - self.current_scale) / 2
                    self.crop_sprite.y = self.tile.y + grid_size * (1 - self.current_scale) / 2
                
                self.crop_sprite.visible = True
            
            return True
        return False

