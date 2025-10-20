"""
Farm Manager - Handles farm setup and tile management
"""
from constants import grid_size
from farm_tile import FarmTile


class FarmManager:
    def __init__(self, game_window):
        self.game_window = game_window
        self.farm_tiles = None
    
    def setup_farm(self):
        """Initialize the farm with tiles (245 pixel border at right for UI)"""
        from constants import farm_batch, game_config
        tiles = []
        map_width = game_config.get('map_width', 50)
        map_height = game_config.get('map_height', 25)
        # Create farm tiles grid
        for i in range(map_width):
            for j in range(map_height):
                x = i * grid_size
                y = j * grid_size
                tile = FarmTile(x, y, farm_batch)
                tiles.append(tile)

        # Center the owned area in the farm grid
        tiles_width = map_width
        tiles_height = map_height
        center_grid_x = tiles_width // 2
        center_grid_y = tiles_height // 2

        # Set owned tiles: 6 columns in center for middle row and row below
        for tile in tiles:
            tile_grid_x = tile.x // grid_size
            tile_grid_y = tile.y // grid_size
            # Create 6x2 area of owned tiles in the center (6 columns, 2 rows)
            # Middle row and the row below it
            if (center_grid_x - 2 <= tile_grid_x <= center_grid_x + 3 and
                center_grid_y <= tile_grid_y <= center_grid_y + 1):
                tile.set_state(1)  # TILE_OWNED

                # Add carrot seed bin at the end of the first owned row (rightmost position)
                if (tile_grid_x == center_grid_x + 3 and tile_grid_y == center_grid_y):
                    from constants import TILE_SEED_BIN, BUILDING_SEED_BIN
                    tile.build_structure(BUILDING_SEED_BIN)
                    tile.store_crop("Carrot", 20)  # Start with 20 carrot seeds - this will create the icon

                # Add barn as second to last tile of the first owned row
                elif (tile_grid_x == center_grid_x + 2 and tile_grid_y == center_grid_y):
                    from constants import TILE_BARN
                    tile.set_state(TILE_BARN)
                    tile.building_type = "barn"

        self.farm_tiles = tiles
        return tiles
    
    def get_tile_at_position(self, grid_x, grid_y):
        """Get the farm tile at the given grid position"""
        if not self.farm_tiles:
            return None
            
        for tile in self.farm_tiles:
            if tile.x == grid_x and tile.y == grid_y:
                return tile
        return None

