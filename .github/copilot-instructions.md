# Copilot Instructions for Farming Game

## Project Overview
This is a 2D farming simulation game built with Python and Pyglet. Players manage farms with tractors, crops, buildings, and a dynamic market system. The game features a tile-based grid system with economic mechanics and automated tractor operations.

## Architecture Patterns

### Manager-Based Architecture
The codebase follows a manager pattern where `GameWindow` delegates to specialized managers:
- `FarmManager` - Farm tiles and layout (3x3 starting area, 50x25 grid)
- `TractorManager` - Multiple tractors with 1-row/3-row modes, job queuing
- `RenderingManager` - Pyglet batches (farm_batch, tractor_batch, ui_batch)
- `UIManager` - Button system and right-panel UI
- `PopupSystem` - Modal dialogs for buildings/seeds/tractors (7 specialized popup classes)

### Configuration-Driven Design
All game data lives in `config/*.json` files:
- `seeds.json` - Crop types, growth times, nutrient requirements
- `fertilizer.json` - Fertilizer types and costs
- `tractor.json` - Tractor speeds and upgrade costs
- `game_config.json` - Building capacities, map size, tile prices

### State Management
- `GameState` - Central state with `Finance` system for transaction tracking
- `Market` - Dynamic pricing that changes every 30 seconds
- Each `FarmTile` maintains its own state (UNOWNED→OWNED→TILLED→PLANTED→GROWING→READY_HARVEST)

## Key Systems

### Tractor Job Queue System
Tractors use a sophisticated queuing system in `tractor_job_queue.py`:
```python
# Queue jobs with row mode preservation
queue.add_job(JobType.TILLING, x, y, num_rows=3)
queue.add_job(JobType.FERTILIZING, x, y, fertilizer_data={'name': 'Compost'})
```
Jobs store metadata like `num_rows` and `fertilizer_data` to maintain context.

### Popup System Architecture
The popup system has 7 specialized handlers:
- `PopupCore` - Base state and scrolling logic
- `PopupBuilding` - Barn/seed bin construction
- `PopupSeeds` - Seed type selection with pagination (6 items per page)
- `PopupFertilizer` - Fertilizer selection (5 items per page)
- `PopupTractor` - Row mode switching and upgrades
- `PopupOverlays` - Visual overlay toggles
- `PopupRenderer` - Centralized drawing with scroll/tooltip support

### Farm Tile System
Each tile has multiple responsibilities handled by separate managers:
- `FarmTileCropManager` - Plant growth, harvesting, nutrient consumption
- `FarmTileNutrientManager` - Soil chemistry (7 nutrients: N, P, K, Ca, Mg, S, water)
- `FarmTileBuildingManager` - Barn/seed bin storage and capacity
- `FarmTileVisualManager` - Sprite rendering and batch management

## Development Patterns

### Error Recovery
The game includes extensive error recovery:
- `rebuild_tractor_batch()` - Recovers from Pyglet graphics errors
- Finance system tracks all transactions with rollback capability
- Popup system handles missing data gracefully

### Input Handling
Input is split across specialized handlers:
- `InputMouseHandler` - Click detection with tile coordinate conversion
- `InputKeyboardHandler` - Seed selection (1-9), mode switching
- `InputTileHandler` - Tile operations based on current mode
- `InputBuildingHandler` - Building placement and validation

### Rendering Order
Uses Pyglet groups for proper draw order:
```python
background_group = pyglet.graphics.Group(order=0)  # Tiles, buildings
icon_group = pyglet.graphics.Group(order=1)        # Icons on buildings
```

## Testing & Debugging
- Run with `python main.py` - prints comprehensive control help
- Terminal commands show various test outputs for pagination, finance system
- Market window (`M` key) shows live price fluctuations
- Financial window shows transaction history and spending categories

## File Organization
- Core game files: `game_window.py`, `game_state.py`, `main.py`
- Managers: `*_manager.py` files handle specific subsystems
- Popup system: `popup_*.py` files for modal interactions
- Input handling: `input_*.py` files for different input types
- Legacy files: `*_original.py`, `*_old.py` preserved for reference

## Common Operations
- Adding new crop types: Update `config/seeds.json` and add tile image
- Adding new buildings: Extend `PopupBuilding` and update tile states
- Adding tractor operations: Extend `JobType` enum and `TractorOperations`
- UI changes: Modify appropriate manager, not `GameWindow` directly