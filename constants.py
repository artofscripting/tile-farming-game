import pyglet
import json
import sys
import os

# Handle PyInstaller bundle path
if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    bundle_dir = sys._MEIPASS
else:
    # Running in normal Python environment - use current directory
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Set pyglet resource path to include our bundle directory and parent directory
pyglet.resource.path = [bundle_dir, os.path.join(bundle_dir, 'tilefarmer')]
pyglet.resource.reindex()

# Load config files
with open(os.path.join(bundle_dir, 'config', 'game_config.json'), 'r') as f:
    game_config = json.load(f)
with open(os.path.join(bundle_dir, 'config', 'seeds.json'), 'r') as f:
    seeds_config = json.load(f)
with open(os.path.join(bundle_dir, 'config', 'fertilizer.json'), 'r') as f:
    fertilizer_config = json.load(f)
with open(os.path.join(bundle_dir, 'config', 'tractor.json'), 'r') as f:
    tractor_config = json.load(f)

# Load our images
farm_tile_image = pyglet.resource.image('img/farm_tile.png')
tilled_image = pyglet.resource.image('img/tilled.png')
tractor_image = pyglet.resource.image('img/tractor.png')

# Scale forest image to tile size (24x24)
forest_image_raw = pyglet.resource.image('img/forest.png')
forest_image = forest_image_raw.get_texture()
forest_image.width = 24
forest_image.height = 24

barn_image = pyglet.resource.image('img/barn.png')
seed_bin_image = pyglet.resource.image('img/seed_bin.png')
unowned_image = pyglet.resource.image('img/unowned.png')
grass_image = pyglet.resource.image('img/grass.png')

# Load crop images
crop_images = {}
for seed in seeds_config:
    try:
        crop_images[seed['name']] = pyglet.resource.image(f"img/{seed['tile_image']}")
    except:
        print(f"Warning: Could not load image img/{seed['tile_image']} for {seed['name']}")

# Create a Batch for our farm tiles
farm_batch = pyglet.graphics.Batch()
# Load tile_size from game_config.json
grid_size = game_config.get('tile_size', 32)
icon_batch = pyglet.graphics.Batch()  # Separate batch for icons - drawn after farm_batch
tractor_batch = pyglet.graphics.Batch()
ui_batch = pyglet.graphics.Batch()

# Rendering groups to control draw order (higher numbers draw on top)
background_group = pyglet.graphics.Group(order=0)  # Background tiles, buildings
icon_group = pyglet.graphics.Group(order=1)        # Icons on top of buildings
forest_image_raw = pyglet.resource.image('img/forest.png')
forest_image = forest_image_raw.get_texture()
forest_image.width = grid_size
forest_image.height = grid_size

# Mouse modes
MOUSE_MODE_NORMAL = 0
MOUSE_MODE_TRACTOR = 1
MOUSE_MODE_BUY_TILES = 2
MOUSE_MODE_PLANT_SEEDS = 3
MOUSE_MODE_HARVEST = 4
MOUSE_MODE_BUILD = 5
MOUSE_MODE_CULTIVATE = 6
MOUSE_MODE_CULTIVATOR = 7
MOUSE_MODE_OVERLAYS = 8

# Overlay types
OVERLAY_NONE = 0
OVERLAY_WEEDS = 1
OVERLAY_WATER = 2
OVERLAY_NITROGEN = 3
OVERLAY_PHOSPHORUS = 4
OVERLAY_POTASSIUM = 5
OVERLAY_CALCIUM = 6
OVERLAY_MAGNESIUM = 7
OVERLAY_SULFUR = 8
OVERLAY_SEED_REQUIREMENTS = 9

# Tile states
TILE_UNOWNED = 0
TILE_OWNED = 1
TILE_TILLED = 2
TILE_PLANTED = 3
TILE_GROWING = 4
TILE_READY_HARVEST = 5
TILE_BARN = 6
TILE_SEED_BIN = 7

# Building types
BUILDING_BARN = 'barn'
BUILDING_SEED_BIN = 'seed_bin'

