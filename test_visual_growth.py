import json
import time
from game_window import GameWindow
from constants import TILE_PLANTED

# Create game and set up a crop
gw = GameWindow(1013, 768, 'Test')

# Set up a tile with a growing crop
tile = gw.farm_tiles[0]
tile.state = TILE_PLANTED

# Manually set up crop manager
tile.crop_manager.crop_type = 'Carrot'
tile.crop_manager.plant_time = time.time() - 1  # Planted 1 second ago
tile.crop_manager.growth_time = 5000  # 5 seconds to grow
tile.crop_manager.current_scale = 0.6  # Partially grown

print('=== Before Save ===')
print(f'Crop type: {tile.crop_manager.crop_type}')
print(f'Plant time: {tile.crop_manager.plant_time}')
print(f'Growth time: {tile.crop_manager.growth_time}')
print(f'Current scale: {tile.crop_manager.current_scale}')
print(f'Tile state: {tile.state}')

# Save game
result = gw.save_game('test_visual_growth.json')
print(f'\nSave result: {result}')

# Check what's saved
with open('test_visual_growth.json', 'r') as f:
    data = json.load(f)
    if 'farm_tiles' in data and data['farm_tiles']:
        tile_data = data['farm_tiles'][0]
        print(f'\n=== Saved Data ===')
        print(f'Crop type: {tile_data.get("crop_type")}')
        print(f'Plant time: {tile_data.get("plant_time")}')
        print(f'Growth time: {tile_data.get("growth_time")}')
        print(f'Current scale: {tile_data.get("current_scale")}')
        print(f'Tile state: {tile_data.get("state")}')

# Create new game and load
print(f'\n=== Loading Game ===')
gw2 = GameWindow(1013, 768, 'Test2')
result = gw2.load_game('test_visual_growth.json')
print(f'Load result: {result}')

# Check loaded tile
loaded_tile = gw2.farm_tiles[0]
print(f'\n=== After Load ===')
print(f'Crop type: {loaded_tile.crop_manager.crop_type}')
print(f'Plant time: {loaded_tile.crop_manager.plant_time}')
print(f'Growth time: {loaded_tile.crop_manager.growth_time}')
print(f'Current scale: {loaded_tile.crop_manager.current_scale}')
print(f'Tile state: {loaded_tile.state}')

# Check sprite scale if it exists
if loaded_tile.crop_manager.crop_sprite:
    print(f'Sprite scale_x: {loaded_tile.crop_manager.crop_sprite.scale_x}')
    print(f'Sprite scale_y: {loaded_tile.crop_manager.crop_sprite.scale_y}')

# Wait a bit and update growth
print(f'\nWaiting 2 seconds and updating growth...')
time.sleep(2)
loaded_tile.crop_manager.update_growth()
print(f'After growth update - Scale: {loaded_tile.crop_manager.current_scale}, State: {loaded_tile.state}')

gw.close()
gw2.close()

