"""
Simplified Game Window - Main window class with manager deleg        # Create UI Info Window
        self.ui_info_window = UIInfoWindow(self)on
"""
import pyglet
import os
import json
from pathlib import Path
from constants import grid_size, MOUSE_MODE_NORMAL, BUILDING_BARN, TILE_PLANTED
from window_setup import WindowSetup
from game_managers import GameManagers
from game_events import GameEvents
from game_rendering import GameRendering
from tooltip_system import TooltipSystem
from popup_system import PopupSystem
from input_handler import InputHandler
from ui_manager import UIManager
from market_window import MarketWindow
from market_history_window import MarketHistoryWindow
from fertilizer_info_window import FertilizerInfoWindow
from ui_info_window import UIInfoWindow
from orders_window import OrdersPopup


class GameWindow(pyglet.window.Window):
    @property
    def farm_tiles(self):
        return self.managers.farm_manager.farm_tiles
    
    @property
    def tractors(self):
        return self.managers.tractor_manager.tractors
    
    @property
    def overlay_manager(self):
        return self.managers.overlay_manager
    
    @property
    def tractor_job_queue(self):
        return self.managers.tractor_job_queue
    def __init__(self, *args, **kwargs):
        from constants import game_config
        ui_border_right = 245
        map_width = game_config.get('map_width', 50)
        map_height = game_config.get('map_height', 25)
        window_width = map_width * grid_size + ui_border_right
        window_height = map_height * grid_size
        
        # Initialize the pyglet window
        super().__init__(width=window_width, height=window_height, caption="A Tile Farming Game", *args, **kwargs)
        
        # Set window icon and position
        try:
            icon = pyglet.image.load('forest.ico')
            self.set_icon(icon)
        except Exception:
            pass
        screen = self.screen
        if screen:
            self.set_location(
                int((screen.width - window_width) / 2),
                int((screen.height - window_height) / 2)
            )
        # Initialize game state first
        from game_state import GameState
        from market import Market
        self.game_state = GameState()
        self.market = Market()
        # Initialize order system with market reference
        self.game_state.order_system.initialize_starting_orders(self.market)
        self.managers = GameManagers(self)
        # Setup the farm tiles
        self.managers.farm_manager.setup_farm()
        self.events = GameEvents(self)
        self.rendering = GameRendering(self)
        self.tooltip_system = TooltipSystem(self)
        self.popup_system = PopupSystem(self)
        self.input_handler = InputHandler(self)
        self.ui_manager = UIManager(self)
        self.market_window = None
        self.market_history_window = None
        self.fertilizer_info_window = None
        self.orders_window = None

        # Initialize UI info window
        self.ui_info_window = UIInfoWindow(self)

        # Initialize game attributes
        self.current_row = 0
        self.active_tractor_index = 0
        self.auto_till = False
        self.mouse_mode = MOUSE_MODE_NORMAL
        self.selected_building = BUILDING_BARN

        # Create custom cursors
        self.tractor_cursor = self.managers.tractor_manager.tractor_cursor

        # Initialize tractor highlighting
        self.managers.tractor_manager.update_tractor_highlighting()

        # Initialize row mode button visibility
        self.ui_manager.update_row_mode_button()

        # Auto-save timer (saves every 2 minutes)
        self.auto_save_timer = 0.0
        self.auto_save_interval = 120.0  # 2 minutes in seconds

        # Notification system
        self.notification_message = None
        self.notification_timer = 0.0
        self.notification_duration = 10.0  # 10 seconds

        # Schedule the update method
        import pyglet
        pyglet.clock.schedule_interval(self.events.update, 1/60.0)
    
    def show_orders_window(self):
        """Show the orders popup"""
        if self.orders_window is None:
            self.orders_window = OrdersPopup(self.game_state, self.game_state.order_system, self)
        self.orders_window.show()
    
    # Delegate methods to managers
    def get_tile_at_position(self, grid_x, grid_y):
        """Get the farm tile at the given grid position"""
        return self.managers.farm_manager.get_tile_at_position(grid_x, grid_y)
    
    def get_active_tractor(self):
        """Get the currently active/selected tractor"""
        return self.managers.tractor_manager.get_active_tractor()
    
    def get_available_tractor(self):
        """Get an available (idle) tractor for a task"""
        return self.managers.tractor_manager.get_available_tractor()
    
    def purchase_tractor(self):
        """Purchase a new tractor if the player can afford it"""
        result = self.managers.tractor_manager.purchase_tractor()
        if result:
            # Update local references
            self.active_tractor_index = self.managers.tractor_manager.active_tractor_index
        return result
    
    def update_tractor_highlighting(self):
        """Update tractor highlighting to show which one is active"""
        self.managers.tractor_manager.update_tractor_highlighting()
    
    def select_next_tractor(self):
        """Select the next tractor in the list"""
        self.managers.tractor_manager.select_next_tractor()
        self.active_tractor_index = self.managers.tractor_manager.active_tractor_index
    
    def select_previous_tractor(self):
        """Select the previous tractor in the list"""
        self.managers.tractor_manager.select_previous_tractor()
        self.active_tractor_index = self.managers.tractor_manager.active_tractor_index
    
    # Utility methods
    def toggle_mode(self, mode, button, cursor):
        """Toggle between different mouse modes"""
        self.mouse_mode = mode if self.mouse_mode != mode else MOUSE_MODE_NORMAL
        self.set_mouse_cursor(cursor if self.mouse_mode == mode else None)
    
    def toggle_market_window(self):
        """Toggle the market window open/closed"""
        if self.market_window is None:
            self.open_market_window()
        else:
            self.close_market_window()
    
    def open_market_window(self):
        """Open the market window"""
        if self.market_window is None:
            self.market_window = MarketWindow(self.market, self)
            print("Market window opened - Press L to close")
    
    def close_market_window(self):
        """Close the market window"""
        if self.market_window is not None:
            self.market_window.close()
            self.market_window = None
            print("Market window closed")
    
    def toggle_market_history_window(self):
        """Toggle the market history window open/closed"""
        if self.market_history_window is None:
            self.open_market_history_window()
        else:
            self.close_market_history_window()
    
    def open_market_history_window(self):
        """Open the market history window"""
        if self.market_history_window is None:
            self.market_history_window = MarketHistoryWindow(self.market, self)
            print("Market history window opened - Press H to close")
    
    def close_market_history_window(self):
        """Close the market history window"""
        if self.market_history_window is not None:
            self.market_history_window.close()
            self.market_history_window = None
            print("Market history window closed")
    
    def show_notification(self, message, duration=None):
        """Show a notification message in the bottom left of the game area"""
        self.notification_message = message
        self.notification_timer = duration if duration is not None else self.notification_duration
    
    def toggle_fertilizer_info_window(self):
        """Toggle the fertilizer info window open/closed"""
        if self.fertilizer_info_window is None:
            self.open_fertilizer_info_window()
        else:
            self.close_fertilizer_info_window()
    
    def open_fertilizer_info_window(self):
        """Open the fertilizer info window"""
        if self.fertilizer_info_window is None:
            self.fertilizer_info_window = FertilizerInfoWindow(self)
            print("Fertilizer info window opened - Press F to close")
    
    def close_fertilizer_info_window(self):
        """Close the fertilizer info window"""
        if self.fertilizer_info_window is not None:
            self.fertilizer_info_window.close()
            self.fertilizer_info_window = None
            print("Fertilizer info window closed")
    
    def get_save_directory(self):
        """Get the save directory path: My Documents/My Games/A Tile Farming Game/"""
        # Get the user's Documents folder
        documents_path = Path.home() / "Documents"
        
        # Create the save directory path
        save_dir = documents_path / "My Games" / "A Tile Farming Game"
        
        # Create the directory if it doesn't exist
        save_dir.mkdir(parents=True, exist_ok=True)
        
        return save_dir
    
    def save_game(self, filename="game_save.json"):
        """Save the complete game state"""
        import json
        try:
            # Get the full path for the save file
            save_dir = self.get_save_directory()
            full_path = save_dir / filename
            
            # Save game state
            self.game_state.save_game_state(str(full_path))
            
            # Get additional data that needs to be saved
            game_data = {}
            
            # Load existing save file and add additional data
            try:
                with open(full_path, 'r') as f:
                    game_data = json.load(f)
            except:
                pass
            
            # Add farm tiles data
            farm_tiles_data = []
            for tile in self.farm_tiles:
                tile_data = {
                    'x': tile.x,
                    'y': tile.y,
                    'state': tile.state,
                    'weeds': tile.weeds,
                    'crop_type': tile.crop_manager.get_crop_type(),
                    'growth_time': tile.crop_manager.growth_time,
                    'plant_time': tile.crop_manager.plant_time,
                    'current_scale': tile.crop_manager.current_scale,
                    'building_type': tile.building_manager.building_type,
                    'stored_crop_type': tile.building_manager.get_stored_crop_type(),
                    'stored_amount': tile.building_manager.get_stored_amount(),
                    'building_capacity': tile.building_manager.get_building_capacity(),
                    'previous_seed_type': tile.building_manager.previous_seed_type,
                    'nutrients': tile.nutrient_manager.nutrients.copy()
                }
                farm_tiles_data.append(tile_data)
            
            # Add tractor data
            tractors_data = []
            for tractor in self.tractors:
                tractor_data = {
                    'x': tractor.x,
                    'y': tractor.y,
                    'target_x': tractor.core.target_x,
                    'target_y': tractor.core.target_y,
                    'moving': tractor.core.moving,
                    'speed': tractor.speed,
                    'is_idle': tractor.is_idle(),
                    'row_direction': tractor.core.row_direction,
                    'mode': tractor.core.mode,
                    'selected_seed': tractor.core.selected_seed,
                    'selected_fertilizer': tractor.core.selected_fertilizer,
                    'cultivated_tiles': list(tractor.core.cultivated_tiles),
                    'additional_rows': tractor.core.additional_rows.copy(),
                    'current_operation': tractor.core.current_operation,
                    'field_width': tractor.core.field_width,
                    'start_x': tractor.core.start_x,
                    'current_seed_type': tractor.core.current_seed_type,
                    'current_fertilizer_data': tractor.core.current_fertilizer_data,
                    'active_rows': tractor.core.active_rows.copy(),
                    'job_harvest_accumulator': tractor.core.job_harvest_accumulator.copy(),
                    'job_fertilizer_accumulator': tractor.core.job_fertilizer_accumulator.copy()
                }
                tractors_data.append(tractor_data)
            
            # Add additional game data
            game_data.update({
                'current_day': getattr(self.market, 'current_day', 0),
                'current_row': self.current_row,
                'active_tractor_index': self.active_tractor_index,
                'auto_till': self.auto_till,
                'mouse_mode': self.mouse_mode,
                'selected_building': self.selected_building,
                'farm_tiles': farm_tiles_data,
                'tractors': tractors_data,
                'tractor_job_queue': self.tractor_job_queue.save_job_data(),
                'order_system': self.game_state.order_system.save_order_data()
            })
            
            # Save complete data
            with open(full_path, 'w') as f:
                json.dump(game_data, f, indent=2)
            
            print(f"💾 Complete game saved to {full_path}")
            self.show_notification("Game Saved!")
            return True
        except Exception as e:
            print(f"❌ Failed to save game: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def auto_save_game(self):
        """Auto-save the game to autosave.json"""
        try:
            result = self.save_game("autosave.json")
            if result:
                save_dir = self.get_save_directory()
                full_path = save_dir / "autosave.json"
                print(f"💾 Auto-saved game to {full_path}")
            return result
        except Exception as e:
            print(f"❌ Auto-save failed: {e}")
            return False
    
    def load_game(self, filename="game_save.json"):
        """Load the complete game state"""
        import json
        try:
            # Get the full path for the save file
            save_dir = self.get_save_directory()
            full_path = save_dir / filename
            
            with open(full_path, 'r') as f:
                game_data = json.load(f)
            
            # Load game state
            self.game_state.load_game_state(str(full_path))
            
            # Load farm tiles data
            if 'farm_tiles' in game_data:
                for i, tile_data in enumerate(game_data['farm_tiles']):
                    if i < len(self.farm_tiles):
                        tile = self.farm_tiles[i]
                        tile.state = tile_data.get('state', tile.state)
                        tile.weeds = tile_data.get('weeds', tile.weeds)
                        
                        # Load crop data
                        crop_type = tile_data.get('crop_type')
                        if crop_type is not None and crop_type != "":
                            tile.crop_manager.restore_crop_state(
                                crop_type,
                                tile_data.get('growth_time', 0),
                                tile_data.get('plant_time', 0),
                                tile_data.get('state', TILE_PLANTED),
                                tile_data.get('current_scale', 0.5)
                            )
                            # Note: update_growth() is not called here to preserve saved state exactly
                        
                        # Load building data
                        if tile_data.get('building_type'):
                            tile.building_manager.building_type = tile_data['building_type']
                            tile.building_manager.stored_crop_type = tile_data.get('stored_crop_type', None)
                            tile.building_manager.stored_amount = tile_data.get('stored_amount', 0)
                            tile.building_manager.building_capacity = tile_data.get('building_capacity', 0)
                            tile.building_manager.previous_seed_type = tile_data.get('previous_seed_type', None)
                        
                        # Load nutrients
                        if 'nutrients' in tile_data:
                            tile.nutrient_manager.nutrients = tile_data['nutrients'].copy()
                        
                        # Update visual state
                        tile.visual_manager.set_state(tile.state)
            
            # Load tractor data
            if 'tractors' in game_data:
                for i, tractor_data in enumerate(game_data['tractors']):
                    if i < len(self.tractors):
                        tractor = self.tractors[i]
                        tractor.x = tractor_data.get('x', tractor.x)
                        tractor.y = tractor_data.get('y', tractor.y)
                        tractor.core.target_x = tractor_data.get('target_x', tractor.core.target_x)
                        tractor.core.target_y = tractor_data.get('target_y', tractor.core.target_y)
                        tractor.core.moving = tractor_data.get('moving', tractor.core.moving)
                        tractor.speed = tractor_data.get('speed', tractor.speed)
                        tractor.core.row_direction = tractor_data.get('row_direction', tractor.core.row_direction)
                        tractor.core.mode = tractor_data.get('mode', tractor.core.mode)
                        tractor.core.selected_seed = tractor_data.get('selected_seed', tractor.core.selected_seed)
                        tractor.core.selected_fertilizer = tractor_data.get('selected_fertilizer', tractor.core.selected_fertilizer)
                        tractor.core.cultivated_tiles = set(tuple(coord) for coord in tractor_data.get('cultivated_tiles', []))
                        tractor.core.additional_rows = tractor_data.get('additional_rows', tractor.core.additional_rows).copy()
                        tractor.core.current_operation = tractor_data.get('current_operation', tractor.core.current_operation)
                        tractor.core.field_width = tractor_data.get('field_width', tractor.core.field_width)
                        tractor.core.start_x = tractor_data.get('start_x', tractor.core.start_x)
                        tractor.core.current_seed_type = tractor_data.get('current_seed_type', tractor.core.current_seed_type)
                        tractor.core.current_fertilizer_data = tractor_data.get('current_fertilizer_data', tractor.core.current_fertilizer_data)
                        tractor.core.active_rows = tractor_data.get('active_rows', tractor.core.active_rows).copy()
                        tractor.core.job_harvest_accumulator = tractor_data.get('job_harvest_accumulator', tractor.core.job_harvest_accumulator).copy()
                        tractor.core.job_fertilizer_accumulator = tractor_data.get('job_fertilizer_accumulator', tractor.core.job_fertilizer_accumulator).copy()
                        
                        # Update sprite position
                        tractor.core.sprite.x = tractor.x
                        tractor.core.sprite.y = tractor.y
            
            # Show tractors that are currently working
            for tractor in self.tractors:
                if tractor.core.current_operation or tractor.core.moving:
                    tractor.core.show()
                else:
                    tractor.core.hide()
            
            # Load additional game data
            self.current_row = game_data.get('current_row', self.current_row)
            self.active_tractor_index = game_data.get('active_tractor_index', self.active_tractor_index)
            self.auto_till = game_data.get('auto_till', self.auto_till)
            self.mouse_mode = game_data.get('mouse_mode', self.mouse_mode)
            self.selected_building = game_data.get('selected_building', self.selected_building)
            
            # Update tractor manager
            self.managers.tractor_manager.active_tractor_index = self.active_tractor_index
            
            # Load order system data
            if 'order_system' in game_data:
                self.game_state.order_system.load_order_data(game_data['order_system'])
            
            # Load tractor job queue data
            if 'tractor_job_queue' in game_data:
                self.tractor_job_queue.load_job_data(game_data['tractor_job_queue'])
            
            # Load market day
            if 'current_day' in game_data:
                self.market.current_day = game_data['current_day']
            
            # Update UI
            if hasattr(self, 'ui_info_window'):
                self.ui_info_window._update_info()
            
            print(f"📂 Complete game loaded from {full_path}")
            self.show_notification("Game Loaded!")
            return True
        except FileNotFoundError:
            print(f"📂 No save file found at {full_path}")
            return False
        except Exception as e:
            print(f"❌ Failed to load game: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def reset_all_buttons(self):
        """Reset all button states"""
        self.ui_manager.reset_all_buttons()
    
    def set_mouse_cursor(self, cursor):
        """Set the mouse cursor"""
        if cursor is None:
            # Reset to default cursor
            super().set_mouse_cursor(self.get_system_mouse_cursor(pyglet.window.Window.CURSOR_DEFAULT))
        elif isinstance(cursor, str):
            # Convert string cursor type to actual cursor object
            super().set_mouse_cursor(self.get_system_mouse_cursor(cursor))
        else:
            # Already a cursor object
            super().set_mouse_cursor(cursor)
    
    def get_system_mouse_cursor(self, cursor_type):
        """Get a system mouse cursor"""
        return super().get_system_mouse_cursor(cursor_type)

