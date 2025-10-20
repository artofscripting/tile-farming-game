import pyglet
from constants import (
    grid_size, crop_images, ui_batch, TILE_BARN, TILE_SEED_BIN,
    BUILDING_BARN, BUILDING_SEED_BIN, game_config, TILE_OWNED
)


class FarmTileBuildingManager:
    """Manages buildings and storage for a farm tile"""

    def __init__(self, tile):
        self.tile = tile
        self.building_type = None
        self.stored_crop_type = None
        self.previous_seed_type = None
        self.stored_amount = 0
        self.building_capacity = 50  # Default capacity for buildings
        self.seed_icon_sprite = None

    def build_structure(self, building_type):
        """Build a structure on this tile"""
        if self.tile.state == TILE_OWNED:
            self.building_type = building_type
            if building_type == BUILDING_BARN:
                self.tile.state = TILE_BARN
                self.building_capacity = 100  # Barns hold more
            elif building_type == BUILDING_SEED_BIN:
                self.tile.state = TILE_SEED_BIN
                self.building_capacity = 50  # Seed bins hold less
            self.tile.set_state(self.tile.state)
            return True
        return False

    def can_store_crop(self, crop_type):
        """Check if this building can store the given crop type"""
        if self.tile.state not in [TILE_BARN, TILE_SEED_BIN]:
            return False
        # Building can store if it's empty or already storing this crop type
        return self.stored_crop_type is None or self.stored_crop_type == crop_type

    def store_crop(self, crop_type, amount=1):
        """Store crops in this building"""
        if not self.can_store_crop(crop_type):
            return False

        space_available = self.building_capacity - self.stored_amount
        amount_to_store = min(amount, space_available)

        if amount_to_store > 0:
            if self.stored_crop_type is None:
                self.stored_crop_type = crop_type
                # Create seed icon sprite for seed bins
                if self.tile.state == TILE_SEED_BIN and crop_type in crop_images:
                    self._create_seed_icon(crop_type)
            self.stored_amount += amount_to_store
            return amount_to_store
        return 0

    def remove_crop(self, amount=1):
        """Remove crops from this building"""
        if self.stored_amount == 0:
            return None, 0

        amount_to_remove = min(amount, self.stored_amount)
        crop_type = self.stored_crop_type
        self.stored_amount -= amount_to_remove

        # If empty, preserve crop type as previous_seed_type for easy refilling
        if self.stored_amount == 0:
            self.previous_seed_type = self.stored_crop_type  # Remember what was in here
            self.stored_crop_type = None
            if self.seed_icon_sprite:
                self.seed_icon_sprite.visible = False
                self.seed_icon_sprite = None

        return crop_type, amount_to_remove

    def _create_seed_icon(self, crop_type):
        """Create and position seed icon sprite centered on the seed bin"""
        if crop_type in crop_images:
            # Remove existing seed icon if present
            if self.seed_icon_sprite:
                self.seed_icon_sprite.visible = False

            # Create new seed icon sprite using ui_batch which draws last to ensure it's on top
            try:
                self.seed_icon_sprite = pyglet.sprite.Sprite(crop_images[crop_type], x=self.tile.x, y=self.tile.y, batch=ui_batch)
            except Exception as e:
                print(f"Error creating seed icon sprite for {crop_type}: {e}")
                # Create sprite without batch as fallback
                self.seed_icon_sprite = pyglet.sprite.Sprite(crop_images[crop_type], x=self.tile.x, y=self.tile.y)

            # Scale the icon to be 80% of the tile height
            icon_size = grid_size * 0.8
            self.seed_icon_sprite.scale_x = icon_size / self.seed_icon_sprite.width
            self.seed_icon_sprite.scale_y = icon_size / self.seed_icon_sprite.height

            # Center the icon on the tile
            # Position sprite so its center aligns with tile center
            self.seed_icon_sprite.x = self.tile.x + (grid_size - icon_size) / 2
            self.seed_icon_sprite.y = self.tile.y + (grid_size - icon_size) / 2

            # Make icon visible
            self.seed_icon_sprite.visible = True

            # Apply current color state
            water_level = self.tile.nutrient_manager.get_nutrient_level('water')
            should_darken = water_level > 100
            dark_color = (217, 217, 217) if should_darken else (255, 255, 255)
            self.seed_icon_sprite.color = dark_color

    def upgrade_seed_bin(self, game_state):
        """Upgrade seed bin capacity if possible"""
        if self.tile.state != TILE_SEED_BIN:
            return False

        upgrade_cost = game_config['seed_bin_upgrade_cost']
        upgrade_amount = game_config['seed_bin_upgrade_amount']
        max_capacity = game_config['seed_bin_upgrade_limit']

        # Check if already at max capacity
        if self.building_capacity >= max_capacity:
            print(f"Seed bin is already at maximum capacity ({max_capacity})")
            return False

        # Check if player can afford upgrade
        if not game_state.can_afford(upgrade_cost):
            print(f"Cannot afford seed bin upgrade (${upgrade_cost})")
            return False

        # Perform upgrade
        if game_state.spend_money(upgrade_cost):
            old_capacity = self.building_capacity
            self.building_capacity = min(self.building_capacity + upgrade_amount, max_capacity)
            actual_increase = self.building_capacity - old_capacity
            print(f"Upgraded seed bin capacity from {old_capacity} to {self.building_capacity} (+{actual_increase}) for ${upgrade_cost}")
            return True

        return False

    def upgrade_barn(self, game_state):
        """Upgrade barn capacity if possible"""
        if self.tile.state != TILE_BARN:
            return False

        upgrade_cost = game_config['barn_upgrade_cost']
        upgrade_amount = game_config['barn_upgrade_amount']
        max_capacity = game_config['barn_upgrade_limit']

        # Check if already at max capacity
        if self.building_capacity >= max_capacity:
            print(f"Barn is already at maximum capacity ({max_capacity})")
            return False

        # Check if player can afford upgrade
        if not game_state.can_afford(upgrade_cost):
            print(f"Cannot afford barn upgrade (${upgrade_cost})")
            return False

        # Perform upgrade
        if game_state.spend_money(upgrade_cost):
            old_capacity = self.building_capacity
            self.building_capacity = min(self.building_capacity + upgrade_amount, max_capacity)
            actual_increase = self.building_capacity - old_capacity
            print(f"Upgraded barn capacity from {old_capacity} to {self.building_capacity} (+{actual_increase}) for ${upgrade_cost}")
            return True

        return False

    def get_stored_crop_type(self):
        """Get the type of crop currently stored"""
        return self.stored_crop_type

    def get_stored_amount(self):
        """Get the amount of crops stored"""
        return self.stored_amount

    def get_building_capacity(self):
        """Get the building's storage capacity"""
        return self.building_capacity

