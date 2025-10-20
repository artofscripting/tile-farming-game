import pyglet
import random
import time
from constants import (
    grid_size, forest_image, farm_tile_image, tilled_image, crop_images,
    barn_image, seed_bin_image, seeds_config, TILE_UNOWNED, TILE_OWNED,
    TILE_TILLED, TILE_PLANTED, TILE_GROWING, TILE_READY_HARVEST,
    TILE_BARN, TILE_SEED_BIN, BUILDING_BARN, BUILDING_SEED_BIN,
    background_group, icon_group, icon_batch, ui_batch
)
from farm_tile_crop_manager import FarmTileCropManager
from farm_tile_nutrient_manager import FarmTileNutrientManager
from farm_tile_building_manager import FarmTileBuildingManager
from farm_tile_visual_manager import FarmTileVisualManager
class FarmTile:
    def __init__(self, x, y, batch):
        self.x = x
        self.y = y
        self.state = TILE_UNOWNED
        self.batch = batch

        # Initialize weeds property
        self.weeds = random.randint(0, 3)  # Start with 0-3 weeds randomly

        # Initialize managers
        self.crop_manager = FarmTileCropManager(self)
        self.nutrient_manager = FarmTileNutrientManager(self)
        self.building_manager = FarmTileBuildingManager(self)
        self.visual_manager = FarmTileVisualManager(self)

        # Set initial visual state
        self.visual_manager.set_state(TILE_UNOWNED)

    # Properties for backward compatibility
    @property
    def crop_type(self):
        return self.crop_manager.get_crop_type()

    @property
    def nutrients(self):
        return self.nutrient_manager.nutrients

    @property
    def building_type(self):
        return self.building_manager.building_type

    @building_type.setter
    def building_type(self, value):
        self.building_manager.building_type = value

    @property
    def stored_crop_type(self):
        return self.building_manager.get_stored_crop_type()

    @property
    def stored_amount(self):
        return self.building_manager.get_stored_amount()

    @stored_amount.setter
    def stored_amount(self, value):
        self.building_manager.stored_amount = value

    @property
    def building_capacity(self):
        return self.building_manager.get_building_capacity()

    @building_capacity.setter
    def building_capacity(self, value):
        self.building_manager.building_capacity = value

    @property
    def seed_icon_sprite(self):
        return self.building_manager.seed_icon_sprite

    @property
    def crop_sprite(self):
        return self.crop_manager.crop_sprite
        
    def plant_crop(self, crop_name):
        return self.crop_manager.plant_crop(crop_name)
    
    def update_growth(self):
        self.crop_manager.update_growth()
    
    def harvest(self):
        return self.crop_manager.harvest(self.nutrient_manager)
    

        
    def build_structure(self, building_type):
        return self.building_manager.build_structure(building_type)

    def can_store_crop(self, crop_type):
        return self.building_manager.can_store_crop(crop_type)

    def store_crop(self, crop_type, amount=1):
        return self.building_manager.store_crop(crop_type, amount)

    def remove_crop(self, amount=1):
        return self.building_manager.remove_crop(amount)
    

    
    def upgrade_seed_bin(self, game_state):
        return self.building_manager.upgrade_seed_bin(game_state)

    def upgrade_barn(self, game_state):
        return self.building_manager.upgrade_barn(game_state)
    
    def set_state(self, new_state):
        self.visual_manager.set_state(new_state)
    
    def cultivate_weeds(self):
        """Reduce weeds to 0 on farmed tiles"""
        if self.state in [TILE_OWNED, TILE_TILLED, TILE_PLANTED, TILE_GROWING, TILE_READY_HARVEST]:
            old_weeds = self.weeds
            self.weeds = 0
            if old_weeds > 0:
                print(f"🌿 Cultivated tile at ({self.x}, {self.y}): reduced {old_weeds} weeds to 0")
                return True
        return False
    
    def grow_weeds(self):
        """Grow weeds by 0.5-5 per day on farmed tiles (owned, tilled, planted, or harvestable)"""
        # Only grow weeds on owned/farmed tiles, not forests or buildings
        if self.state in [TILE_OWNED, TILE_TILLED, TILE_PLANTED, TILE_GROWING, TILE_READY_HARVEST]:
            import random
            # Generate random weed growth between 0.5 and 5.0
            weed_growth = random.uniform(0.5, 5.0)
            self.weeds += weed_growth
            # Cap weeds at a reasonable maximum (e.g., 50)
            self.weeds = min(50.0, self.weeds)
            return weed_growth
        return 0
    
    def update_visual_appearance(self):
        self.visual_manager.update_visual_appearance()

