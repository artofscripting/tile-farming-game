import json
import time
from game_window import GameWindow
from constants import TILE_OWNED, TILE_TILLED

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
tractor.core.field_width = 72  # 3 tiles wide
tractor.core.start_x = 0
tractor.core.mode = 'till'
tractor.core.active_rows = [0]  # Working on row 0
tractor.core.cultivated_tiles = {(0, 0)}  # Already tilled first tile

print("=== Before Save ===")
print(f"Tractor position: ({tractor.x}, {tractor.y})")
print(f"Tractor target: ({tractor.core.target_x}, {tractor.core.target_y})")
print(f"Tractor moving: {tractor.core.moving}")
print(f"Current operation: {tractor.core.current_operation}")
print(f"Field width: {tractor.core.field_width}")
print(f"Active rows: {tractor.core.active_rows}")
print(f"Cultivated tiles: {tractor.core.cultivated_tiles}")

# Save game
result = gw.save_game('test_tractor_working.json')
print(f"\nSave result: {result}")

# Check what's saved
with open('test_tractor_working.json', 'r') as f:
    data = json.load(f)
    if 'tractors' in data and data['tractors']:
        tractor_data = data['tractors'][0]
        print("\n=== Saved Tractor Data ===")
        print(f"Position: ({tractor_data.get('x')}, {tractor_data.get('y')})")
        print(f"Target: ({tractor_data.get('target_x')}, {tractor_data.get('target_y')})")
        print(f"Moving: {tractor_data.get('moving')}")
        print(f"Current operation: {tractor_data.get('current_operation')}")
        print(f"Field width: {tractor_data.get('field_width')}")
        print(f"Active rows: {tractor_data.get('active_rows')}")
        print(f"Cultivated tiles: {tractor_data.get('cultivated_tiles')}")

# Create new game and load
print("\n=== Loading Game ===")
gw2 = GameWindow(1013, 768, 'Test2')
result = gw2.load_game('test_tractor_working.json')
print(f"Load result: {result}")

# Check loaded tractor
loaded_tractor = gw2.tractors[0]
print("\n=== After Load ===")
print(f"Tractor position: ({loaded_tractor.x}, {loaded_tractor.y})")
print(f"Tractor target: ({loaded_tractor.core.target_x}, {loaded_tractor.core.target_y})")
print(f"Tractor moving: {loaded_tractor.core.moving}")
print(f"Current operation: {loaded_tractor.core.current_operation}")
print(f"Field width: {loaded_tractor.core.field_width}")
print(f"Active rows: {loaded_tractor.core.active_rows}")
print(f"Cultivated tiles: {loaded_tractor.core.cultivated_tiles}")

# Verify the tractor can continue working
print("\n=== Testing Continued Operation ===")
# Simulate some time passing and update
initial_x = loaded_tractor.x
time.sleep(0.1)  # Brief pause
# The tractor should still be moving towards its target
print(f"Tractor still moving after load: {loaded_tractor.core.moving}")
print(f"Target still set: ({loaded_tractor.core.target_x}, {loaded_tractor.core.target_y})")

gw.close()
gw2.close()

