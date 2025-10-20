"""
Represents a single tile on the farm grid.
Handles tile states, crop management, and visual representation.
Main coordinator for all tile-related functionality.
"""
import time
import pyglet
from constants import (
    forest_image, farm_tile_image, tilled_image, unowned_image, grass_image,
    crop_images, seed_icons, TILE_FOREST, TILE_UNOWNED, TILE_OWNED, TILE_TILLED,
    TILE_PLANTED, TILE_READY_HARVEST, seeds_config, grid_size, ui_batch,
    barn_image, seed_bin_image, building_prices, building_upgrade_costs
)

# Import the managers
from farm_tile_crop_manager import CropManager
from farm_tile_building_manager import BuildingManager  
from farm_tile_nutrient_manager import NutrientManager
from farm_tile_visual_manager import VisualManager


class FarmTile:
    def __init__(self, x, y, batch):
        self.x = x
        self.y = y
        self.state = TILE_UNOWNED
        self.batch = batch
        
        # Basic tile properties
        self.weed_level = 0
        self.water_level = 50
        self.previous_crop_type = None
        
        # Initialize managers - these handle all the complex logic
        self.nutrient_manager = NutrientManager(self)
        self.visual_manager = VisualManager(self)
        self.crop_manager = CropManager(self)
        self.building_manager = BuildingManager(self)
        
        # Create the base sprite through visual manager
        self.base_sprite = self.visual_manager.create_base_sprite(batch)
        
        # Initialize with unowned state visual
        self.set_state(TILE_UNOWNED)
    
    def set_state(self, new_state):
        """Change the tile state and update visuals"""
        self.state = new_state
        self.visual_manager.update_visual_appearance()
    
    def purchase(self):
        """Purchase this tile (convert from forest to owned)"""
        if self.state == TILE_FOREST:
            self.set_state(TILE_OWNED)
            return True
        return False
    
    def till(self):
        """Till the soil for planting"""
        if self.state == TILE_OWNED:
            self.set_state(TILE_TILLED)
            return True
        return False
    
    def plant_crop(self, crop_name):
        """Plant a crop on this tile"""
        return self.crop_manager.plant_crop(crop_name)
    
    def update_growth(self):
        """Update crop growth state"""
        self.crop_manager.update_growth()
    
    def harvest(self):
        """Harvest the crop and return crop name and reward"""
        crop_name, reward = self.crop_manager.harvest()
        if crop_name:
            self.previous_crop_type = crop_name
        return crop_name, reward
    
    def can_build_barn(self):
        """Check if barn can be built on this tile"""
        return self.building_manager.can_build_barn()
    
    def can_build_seed_bin(self):
        """Check if seed bin can be built on this tile"""
        return self.building_manager.can_build_seed_bin()
    
    def build_barn(self):
        """Build a barn on this tile"""
        success = self.building_manager.build_barn()
        if success:
            self.visual_manager.update_visual_appearance()
        return success
    
    def build_seed_bin(self):
        """Build a seed bin on this tile"""
        success = self.building_manager.build_seed_bin()
        if success:
            self.visual_manager.update_visual_appearance()
        return success
    
    def can_store_crop(self, crop_type):
        """Check if we can store more of this crop type"""
        return self.building_manager.can_store_crop(crop_type)
    
    def store_crop(self, crop_type):
        """Store a crop in this building"""
        return self.building_manager.store_crop(crop_type)
    
    def remove_crop(self, crop_type, amount=1):
        """Remove crop from storage"""
        return self.building_manager.remove_crop(crop_type, amount)
    
    def get_storage_info(self):
        """Get current storage information"""
        return self.building_manager.get_storage_info()
    
    def create_seed_icon(self, seed_name, count):
        """Create or update seed icon for this tile"""
        return self.visual_manager.create_seed_icon(seed_name, count)
    
    def can_upgrade_building(self):
        """Check if building can be upgraded"""
        return self.building_manager.can_upgrade()
    
    def start_building_upgrade(self):
        """Start upgrading the building"""
        return self.building_manager.start_upgrade()
    
    def complete_building_upgrade(self):
        """Complete the building upgrade"""
        success = self.building_manager.complete_upgrade()
        if success:
            self.visual_manager.update_visual_appearance()
        return success
    
    def cultivate_weeds(self):
        """Cultivate weeds on this tile"""
        if self.state == TILE_OWNED:
            # Increase weed level
            self.weed_level = min(100, self.weed_level + 20)
            self.visual_manager.cultivate_weeds()
            return True
        return False
    
    def get_nutrient_info(self):
        """Get nutrient information"""
        return self.nutrient_manager.get_nutrients()
    
    def add_nutrients(self, nitrogen=0, phosphorus=0, potassium=0):
        """Add nutrients to the soil"""
        self.nutrient_manager.add_nutrients(nitrogen, phosphorus, potassium)
        self.visual_manager.update_visual_appearance()
    
    def apply_fertilizer(self, fertilizer_type, amount=1):
        """Apply fertilizer to boost nutrients"""
        success = self.nutrient_manager.apply_fertilizer(fertilizer_type, amount)
        if success:
            self.visual_manager.update_visual_appearance()
        return success
    
    def get_nutrient_status_for_crop(self, crop_name):
        """Get nutrient status information for a specific crop"""
        return self.nutrient_manager.get_nutrient_status_for_crop(crop_name)
    
    def update_visual_appearance(self):
        """Update the visual appearance of the tile"""
        self.visual_manager.update_visual_appearance()
    
    def set_water_level(self, level):
        """Set the water level for this tile"""
        self.water_level = max(0, min(100, level))
        self.visual_manager.update_visual_appearance()
    
    def add_water(self, amount):
        """Add water to this tile"""
        self.set_water_level(self.water_level + amount)
    
    # Properties for backward compatibility
    @property
    def crop_type(self):
        """Get the current crop type"""
        return self.crop_manager.crop_type
    
    @property
    def building_type(self):
        """Get the current building type"""
        return self.building_manager.building_type
    
    @property
    def storage(self):
        """Get the current storage dict"""
        return self.building_manager.storage
    
    @property
    def max_storage(self):
        """Get the maximum storage capacity"""
        return self.building_manager.max_storage
    
    @property
    def is_upgrading(self):
        """Check if building is currently upgrading"""
        return self.building_manager.is_upgrading
    
    # Legacy nutrient properties for backward compatibility
    @property
    def nitrogen(self):
        return self.nutrient_manager.nitrogen
    
    @property
    def phosphorus(self):
        return self.nutrient_manager.phosphorus
    
    @property
    def potassium(self):
        return self.nutrient_manager.potassium

