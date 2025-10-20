import pyglet
from constants import (
    grid_size, forest_image, farm_tile_image, tilled_image, barn_image,
    background_group, TILE_UNOWNED, TILE_OWNED, TILE_TILLED, TILE_BARN, TILE_SEED_BIN,
    TILE_PLANTED, TILE_GROWING, TILE_READY_HARVEST
)


class FarmTileVisualManager:
    """Manages visual sprites and appearance for a farm tile"""

    def __init__(self, tile):
        self.tile = tile
        self.forest_sprite = None
        self.farm_sprite = None
        self.tilled_sprite = None
        self.barn_sprite = None
        self.seed_bin_bg = None
        self.barn_border = None
        self.seed_bin_border = None
        self._create_sprites()

    def _create_sprites(self):
        """Create all the visual sprites for the tile"""
        # Create forest sprite for unowned tile
        self.forest_sprite = pyglet.sprite.Sprite(forest_image, x=self.tile.x, y=self.tile.y,
                                                 batch=self.tile.batch, group=background_group)
        self.forest_sprite.scale_x = grid_size / self.forest_sprite.width
        self.forest_sprite.scale_y = grid_size / self.forest_sprite.height

        # Create sprites for owned and tilled states (initially hidden)
        self.farm_sprite = pyglet.sprite.Sprite(farm_tile_image, x=self.tile.x, y=self.tile.y,
                                               batch=self.tile.batch, group=background_group)
        self.farm_sprite.scale_x = grid_size / self.farm_sprite.width
        self.farm_sprite.scale_y = grid_size / self.farm_sprite.height
        self.farm_sprite.visible = False

        self.tilled_sprite = pyglet.sprite.Sprite(tilled_image, x=self.tile.x, y=self.tile.y,
                                                 batch=self.tile.batch, group=background_group)
        self.tilled_sprite.scale_x = grid_size / self.tilled_sprite.width
        self.tilled_sprite.scale_y = grid_size / self.tilled_sprite.height
        self.tilled_sprite.visible = False

        # Building sprites (initially hidden)
        self.barn_sprite = pyglet.sprite.Sprite(barn_image, x=self.tile.x, y=self.tile.y,
                                               batch=self.tile.batch, group=background_group)
        self.barn_sprite.scale_x = grid_size / self.barn_sprite.width
        self.barn_sprite.scale_y = grid_size / self.barn_sprite.height
        self.barn_sprite.visible = False
        # 2 pixel black border for barn (outline, not filled)
        self.barn_border_lines = [
            pyglet.shapes.Line(self.tile.x, self.tile.y, self.tile.x + grid_size, self.tile.y, thickness=2, color=(0,0,0), batch=self.tile.batch),
            pyglet.shapes.Line(self.tile.x + grid_size, self.tile.y, self.tile.x + grid_size, self.tile.y + grid_size, thickness=2, color=(0,0,0), batch=self.tile.batch),
            pyglet.shapes.Line(self.tile.x + grid_size, self.tile.y + grid_size, self.tile.x, self.tile.y + grid_size, thickness=2, color=(0,0,0), batch=self.tile.batch),
            pyglet.shapes.Line(self.tile.x, self.tile.y + grid_size, self.tile.x, self.tile.y, thickness=2, color=(0,0,0), batch=self.tile.batch)
        ]
        for line in self.barn_border_lines:
            line.visible = False

        # Seed bin icon sprite (initially hidden)
        from constants import seed_bin_image
        self.seed_bin_sprite = pyglet.sprite.Sprite(seed_bin_image, x=self.tile.x, y=self.tile.y,
                                                   batch=self.tile.batch, group=background_group)
        self.seed_bin_sprite.scale_x = grid_size / self.seed_bin_sprite.width
        self.seed_bin_sprite.scale_y = grid_size / self.seed_bin_sprite.height
        self.seed_bin_sprite.visible = False
        # 2 pixel black border for seed bin (outline, not filled)
        self.seed_bin_border_lines = [
            pyglet.shapes.Line(self.tile.x, self.tile.y, self.tile.x + grid_size, self.tile.y, thickness=2, color=(0,0,0), batch=self.tile.batch),
            pyglet.shapes.Line(self.tile.x + grid_size, self.tile.y, self.tile.x + grid_size, self.tile.y + grid_size, thickness=2, color=(0,0,0), batch=self.tile.batch),
            pyglet.shapes.Line(self.tile.x + grid_size, self.tile.y + grid_size, self.tile.x, self.tile.y + grid_size, thickness=2, color=(0,0,0), batch=self.tile.batch),
            pyglet.shapes.Line(self.tile.x, self.tile.y + grid_size, self.tile.x, self.tile.y, thickness=2, color=(0,0,0), batch=self.tile.batch)
        ]
        for line in self.seed_bin_border_lines:
            line.visible = False

    def set_state(self, new_state):
        """Update visual state based on tile state"""
        self.tile.state = new_state

        # Hide all visuals first
        self.forest_sprite.visible = False
        self.farm_sprite.visible = False
        self.tilled_sprite.visible = False
        self.barn_sprite.visible = False
        for line in self.barn_border_lines:
            line.visible = False
        self.seed_bin_sprite.visible = False
        for line in self.seed_bin_border_lines:
            line.visible = False
        if self.tile.building_manager.seed_icon_sprite:
            self.tile.building_manager.seed_icon_sprite.visible = False

        # Determine if tile should be darkened (water > 100)
        water_level = self.tile.nutrient_manager.get_nutrient_level('water')
        should_darken = water_level > 100
        # 70% of 255 = 179 (30% darker for watered tiles)
        dark_color = (179, 179, 179) if should_darken else (255, 255, 255)

        # Show appropriate visual based on state
        if new_state == TILE_UNOWNED:
            self.forest_sprite.visible = True
            # Apply 25% darker tint to unowned tiles (75% of 255 = 191)
            self.forest_sprite.color = (48, 96, 48)  # 25% darker green tint
        elif new_state == TILE_OWNED:
            self.farm_sprite.visible = True
            self.farm_sprite.color = dark_color
        elif new_state == TILE_TILLED:
            self.tilled_sprite.visible = True
            self.tilled_sprite.color = dark_color
        elif new_state == TILE_BARN:
            self.barn_sprite.visible = True
            for line in self.barn_border_lines:
                line.visible = True
            self.barn_sprite.color = dark_color
        elif new_state == TILE_SEED_BIN:
            self.seed_bin_sprite.visible = True
            for line in self.seed_bin_border_lines:
                line.visible = True
            self.seed_bin_sprite.color = dark_color
            # Show seed icon if there's a stored crop type
            if self.tile.building_manager.seed_icon_sprite and self.tile.building_manager.stored_crop_type:
                self.tile.building_manager.seed_icon_sprite.visible = True
                self.tile.building_manager.seed_icon_sprite.color = dark_color
        elif new_state in [TILE_PLANTED, TILE_GROWING, TILE_READY_HARVEST]:
            self.tilled_sprite.visible = True  # Show tilled ground underneath
            self.tilled_sprite.color = dark_color
            if self.tile.crop_manager.crop_sprite:
                self.tile.crop_manager.crop_sprite.visible = True
                self.tile.crop_manager.crop_sprite.color = dark_color

    def update_visual_appearance(self):
        """Update the visual appearance based on current water levels"""
        water_level = self.tile.nutrient_manager.get_nutrient_level('water')
        should_darken = water_level > 100
        dark_color = (217, 217, 217) if should_darken else (255, 255, 255)  # 85% of 255 = 217 (15% darker)

        # Apply color to all sprites (except unowned tiles which have special green tint)
        if self.tile.state == TILE_UNOWNED:
            self.forest_sprite.color = (64, 128, 64)  # 50% dark green tint for unowned tiles
        else:
            self.forest_sprite.color = dark_color
        self.farm_sprite.color = dark_color
        self.tilled_sprite.color = dark_color
        self.barn_sprite.color = dark_color
        self.seed_bin_sprite.color = dark_color
        if self.tile.building_manager.seed_icon_sprite:
            self.tile.building_manager.seed_icon_sprite.color = dark_color
        if self.tile.crop_manager.crop_sprite:
            self.tile.crop_manager.crop_sprite.color = dark_color

