import json
import time
from game_window import GameWindow
from constants import TILE_OWNED

# Create game and set up a tractor working on an operation
gw = GameWindow(1013, 768, 'Test')

# Set up some tiles for the tractor to work on
tile1 = gw.farm_tiles[0]
tile1.state = TILE_OWNED
tile2 = gw.farm_tiles[1]
tile2.state = TILE_OWNED

# Get the tractor and set it up to be working
tractor = gw.tractors[0]

# Manually set up tractor to be in the middle of an operation
tractor.x = 24  # Position it at first tile
tractor.y = 0
tractor.core.target_x = 48  # Moving towards second tile
tractor.core.target_y = 0
tractor.core.moving = True  # Tractor is actively moving
tractor.core.current_operation = 'tilling'
tractor.core.field_width = 72
tractor.core.start_x = 0
tractor.core.mode = 'till'
tractor.core.active_rows = [0]
tractor.core.cultivated_tiles = {(0, 0)}

print("=== Before Save ===")
print(f"Tractor position: ({tractor.x}, {tractor.y})")
print(f"Tractor moving: {tractor.core.moving}")
print(f"Current operation: {tractor.core.current_operation}")
print(f"Sprite visible: {tractor.core.sprite.visible}")

# Save game
result = gw.save_game('test_tractor_visibility.json')
print(f"\nSave result: {result}")

# Create new game and load
print("\n=== Loading Game ===")
gw2 = GameWindow(1013, 768, 'Test2')
result = gw2.load_game('test_tractor_visibility.json')
print(f"Load result: {result}")

# Check loaded tractor visibility
loaded_tractor = gw2.tractors[0]
print("\n=== After Load ===")
print(f"Tractor position: ({loaded_tractor.x}, {loaded_tractor.y})")
print(f"Tractor moving: {loaded_tractor.core.moving}")
print(f"Current operation: {loaded_tractor.core.current_operation}")
print(f"Sprite visible: {loaded_tractor.core.sprite.visible}")

# Test with idle tractor too
print("\n=== Testing Idle Tractor ===")
idle_tractor = gw2.tractors[1] if len(gw2.tractors) > 1 else gw2.tractors[0]
if idle_tractor != loaded_tractor:
    print(f"Idle tractor sprite visible: {idle_tractor.core.sprite.visible}")
else:
    print("Only one tractor available")

gw.close()
gw2.close()

