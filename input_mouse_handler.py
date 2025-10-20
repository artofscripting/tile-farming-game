"""
Mouse input handling and button clicks
"""
import pyglet
from constants import (
    grid_size, MOUSE_MODE_NORMAL, MOUSE_MODE_TRACTOR, MOUSE_MODE_BUY_TILES, 
    MOUSE_MODE_PLANT_SEEDS, MOUSE_MODE_HARVEST, MOUSE_MODE_BUILD, MOUSE_MODE_CULTIVATE, 
    MOUSE_MODE_CULTIVATOR, TILE_BARN, TILE_SEED_BIN, OVERLAY_NONE
)


class MouseHandler:
    """Handles mouse input events and button clicks"""
    
    def __init__(self, game_window):
        self.game_window = game_window
        # Double-click detection
        self.last_click_time = 0
        self.last_click_x = 0
        self.last_click_y = 0
        self.double_click_threshold = 0.3  # seconds
    
    def handle_mouse_press(self, x, y, button, modifiers):
        """Handle mouse button presses"""
        current_time = pyglet.clock.get_default().time()
        
        # Check for double-click
        is_double_click = (current_time - self.last_click_time < self.double_click_threshold and
                          abs(x - self.last_click_x) < 10 and
                          abs(y - self.last_click_y) < 10)
        
        # Update last click info
        self.last_click_time = current_time
        self.last_click_x = x
        self.last_click_y = y
        
        if button == pyglet.window.mouse.LEFT:
            return self._handle_left_click(x, y, modifiers, is_double_click)
        elif button == pyglet.window.mouse.RIGHT:
            return self._handle_right_click(x, y, modifiers)
import pyglet
from constants import (
    grid_size, MOUSE_MODE_NORMAL, MOUSE_MODE_TRACTOR, MOUSE_MODE_BUY_TILES, 
    MOUSE_MODE_PLANT_SEEDS, MOUSE_MODE_HARVEST, MOUSE_MODE_BUILD, MOUSE_MODE_CULTIVATE, 
    MOUSE_MODE_CULTIVATOR, TILE_BARN, TILE_SEED_BIN, OVERLAY_NONE
)


class MouseHandler:
    """Handles mouse input events and button clicks"""
    
    def __init__(self, game_window):
        self.game_window = game_window
        # Double-click detection
        self.last_click_time = 0
        self.last_click_x = 0
        self.last_click_y = 0
        self.double_click_threshold = 0.3  # seconds
    
    def handle_mouse_press(self, x, y, button, modifiers):
        """Handle mouse button presses"""
        current_time = pyglet.clock.get_default().time()
        
        # Check for double-click
        is_double_click = (current_time - self.last_click_time < self.double_click_threshold and
                          abs(x - self.last_click_x) < 10 and
                          abs(y - self.last_click_y) < 10)
        
        # Update last click info
        self.last_click_time = current_time
        self.last_click_x = x
        self.last_click_y = y
        
        if button == pyglet.window.mouse.LEFT:
            return self._handle_left_click(x, y, modifiers, is_double_click)
        elif button == pyglet.window.mouse.RIGHT:
            return self._handle_right_click(x, y, modifiers)
    
    def _handle_left_click(self, x, y, modifiers, is_double_click=False):
        """Handle left mouse button clicks"""
        # Check button clicks first
        if self._handle_ui_button_clicks(x, y):
            return
        
        # Handle popup interactions
        if self.game_window.popup_system.handle_click(x, y):
            return  # Popup handled the click
        
        # Handle tile interactions
        grid_x = int(x // grid_size) * grid_size
        grid_y = int(y // grid_size) * grid_size
        
        if 0 <= grid_y < self.game_window.height and 0 <= grid_x < self.game_window.width:
            tile = self.game_window.get_tile_at_position(grid_x, grid_y)
            if tile:
                # Import here to avoid circular import
                from input_tile_handler import TileInteractionHandler
                tile_handler = TileInteractionHandler(self.game_window)
                tile_handler.handle_tile_interaction(tile, grid_x, grid_y, modifiers, is_double_click)
    
    def _handle_right_click(self, x, y, modifiers):
        """Handle right mouse button clicks"""
        # Check if a popup is showing and close it first
        if self.game_window.popup_system.is_showing_popup():
            self.game_window.popup_system.close_popups()
            print("Popup closed with right-click")
            return
        
        # Check if an overlay is active and close it first
        if (hasattr(self.game_window, 'overlay_manager') and 
            self.game_window.overlay_manager.current_overlay != OVERLAY_NONE):
            self.game_window.overlay_manager.set_overlay(OVERLAY_NONE)
            print("Overlay closed with right-click")
            return
        
        # Check for queued job cancellation first (works in any mode)
        grid_x = int(x // grid_size) * grid_size
        grid_y = int(y // grid_size) * grid_size
        
        if (0 <= grid_y < self.game_window.height and 0 <= grid_x < self.game_window.width and
            hasattr(self.game_window, 'tractor_job_queue')):
            # Try to cancel a queued job at this position
            if self.game_window.tractor_job_queue.cancel_job_at_position(grid_x, grid_y):
                return  # Job cancelled, don't do other right-click actions
        
        # Right-click exits tool mode and returns to normal mode
        if self.game_window.mouse_mode != MOUSE_MODE_NORMAL:
            self.game_window.mouse_mode = MOUSE_MODE_NORMAL
            self.game_window.reset_all_buttons()
            self.game_window.set_mouse_cursor(None)
            print("Exited tool mode")
            return
        
        # Right-click for seed bin purchases and barn selling (only in normal mode)
        if 0 <= grid_y < self.game_window.height and 0 <= grid_x < self.game_window.width:
            tile = self.game_window.get_tile_at_position(grid_x, grid_y)
            if tile and tile.state == TILE_SEED_BIN:
                # Import here to avoid circular import
                from input_building_handler import BuildingInteractionHandler
                building_handler = BuildingInteractionHandler(self.game_window)
                building_handler.buy_seeds_from_bin(tile, modifiers)
            elif tile and tile.state == TILE_BARN:
                # Import here to avoid circular import
                from input_building_handler import BuildingInteractionHandler
                building_handler = BuildingInteractionHandler(self.game_window)
                building_handler.handle_barn_right_click(tile, modifiers)
    
    def _handle_ui_button_clicks(self, x, y):
        """Handle UI button clicks and return True if a button was clicked"""
        # Check all UI buttons
        if self.game_window.tractor_button.contains_point(x, y):
            self.game_window.ui_manager.toggle_mode(MOUSE_MODE_TRACTOR, self.game_window.tractor_button, pyglet.window.Window.CURSOR_CROSSHAIR)
            return True
        elif self.game_window.buy_tiles_button.contains_point(x, y):
            self.game_window.ui_manager.toggle_mode(MOUSE_MODE_BUY_TILES, self.game_window.buy_tiles_button, pyglet.window.Window.CURSOR_HAND)
            return True
        elif self.game_window.plant_seeds_button.contains_point(x, y):
            # Show seed bin selection popup instead of directly entering plant mode
            self.game_window.popup_system.show_seed_bin_selection_popup()
            return True
        elif self.game_window.harvest_button.contains_point(x, y):
            self.game_window.ui_manager.toggle_mode(MOUSE_MODE_HARVEST, self.game_window.harvest_button, pyglet.window.Window.CURSOR_HAND)
            return True
        elif self.game_window.build_button.contains_point(x, y):
            self.game_window.popup_system.show_building_selection_popup()
            return True
        elif self.game_window.cultivate_button.contains_point(x, y):
            self.game_window.popup_system.show_fertilizer_selection_popup()
            return True
        elif self.game_window.cultivator_button.contains_point(x, y):
            self.game_window.ui_manager.toggle_mode(MOUSE_MODE_CULTIVATOR, self.game_window.cultivator_button, pyglet.window.Window.CURSOR_HAND)
            return True
        elif self.game_window.upgrade_tractor_button.contains_point(x, y):
            self.game_window.popup_system.show_tractor_upgrade_popup()
            return True
        elif self.game_window.market_history_button.contains_point(x, y):
            self.game_window.open_market_history_window()
            return True
        elif self.game_window.live_market_button.contains_point(x, y):
            self.game_window.open_market_window()
            return True
        elif self.game_window.overlays_button.contains_point(x, y):
            self.game_window.popup_system.show_overlay_selection_popup()
            return True
        elif self.game_window.fertilizer_info_button.contains_point(x, y):
            self.game_window.open_fertilizer_info_window()
            return True
        elif (hasattr(self.game_window, 'row_mode_toggle_button') and 
              self.game_window.row_mode_toggle_button.visible and 
              self.game_window.row_mode_toggle_button.contains_point(x, y)):
            self.game_window.ui_manager.toggle_row_mode()
            return True
        elif (hasattr(self.game_window, 'financial_button') and 
              self.game_window.financial_button.contains_point(x, y)):
            self.game_window.ui_manager.toggle_financial_window()
            return True
        elif (hasattr(self.game_window, 'orders_button') and 
              self.game_window.orders_button.contains_point(x, y)):
            self.game_window.show_orders_window()
            return True
        elif (hasattr(self.game_window, 'save_button') and 
              self.game_window.save_button.contains_point(x, y)):
            self.game_window.save_game()
            return True
        elif (hasattr(self.game_window, 'load_button') and 
              self.game_window.load_button.contains_point(x, y)):
            self.game_window.load_game()
            return True
        
        return False

