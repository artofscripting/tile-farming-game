import pyglet
from constants import (
    ui_batch, game_config, MOUSE_MODE_NORMAL, MOUSE_MODE_TRACTOR, 
    MOUSE_MODE_BUY_TILES, MOUSE_MODE_PLANT_SEEDS, MOUSE_MODE_HARVEST, MOUSE_MODE_BUILD, MOUSE_MODE_CULTIVATE, MOUSE_MODE_CULTIVATOR
)
from button import Button
from financial_window import FinancialSummaryWindow


class UIManager:
    def __init__(self, game_window):
        self.game_window = game_window
        self.financial_window = FinancialSummaryWindow(game_window)
        self.create_buttons()
    
    def create_buttons(self):
        """Create UI buttons in the right panel area"""
        # Position buttons in the right panel area
        button_x = self.game_window.width - 225  # 10 pixels from right edge
        button_width = 215  # Slightly narrower to fit in panel with good margins
        button_height = 35
        
        # Stack buttons vertically in the right panel
        self.game_window.buy_tiles_button = Button(
            button_x, self.game_window.height - 50, button_width, button_height, 
            "Buy Tiles", ui_batch
        )
        self.game_window.tractor_button = Button(
            button_x, self.game_window.height - 90, button_width, button_height, 
            "Plow", ui_batch
        )
        self.game_window.plant_seeds_button = Button(
            button_x, self.game_window.height - 130, button_width, button_height, 
            "Planter", ui_batch
        )
        self.game_window.cultivate_button = Button(
            button_x, self.game_window.height - 170, button_width, button_height, 
            "Fertilizer", ui_batch
        )
        self.game_window.cultivator_button = Button(
            button_x, self.game_window.height - 210, button_width, button_height, 
            "Cultivator", ui_batch
        )
        self.game_window.harvest_button = Button(
            button_x, self.game_window.height - 250, button_width, button_height, 
            "Harvest", ui_batch
        )
        self.game_window.build_button = Button(
            button_x, self.game_window.height - 290, button_width, button_height, 
            "Build", ui_batch
        )
        self.game_window.upgrade_tractor_button = Button(
            button_x, self.game_window.height - 330, button_width, button_height, 
            "Upgrade Tractor", ui_batch
        )
        self.game_window.market_history_button = Button(
            button_x, self.game_window.height - 370, button_width, button_height, 
            "Market History", ui_batch
        )
        self.game_window.live_market_button = Button(
            button_x, self.game_window.height - 410, button_width, button_height, 
            "Live Market", ui_batch
        )
        self.game_window.overlays_button = Button(
            button_x, self.game_window.height - 450, button_width, button_height, 
            "Overlays", ui_batch
        )
        
        # Fertilizer Info button
        self.game_window.fertilizer_info_button = Button(
            button_x, self.game_window.height - 490, button_width, button_height, 
            "Fertilizer Info", ui_batch
        )
        
        # Row mode toggle button (only visible after 3-row upgrade)
        self.game_window.row_mode_toggle_button = Button(
            button_x, 10 + button_height, button_width, button_height,
            "Toggle Row Mode", ui_batch
        )
        # Initially hidden
        self.game_window.row_mode_toggle_button.visible = False
        
        # Financial Summary button
        self.game_window.financial_button = Button(
            button_x, self.game_window.height - 530, button_width, button_height,
            "Financial Summary", ui_batch
        )
        
        # Orders button
        self.game_window.orders_button = Button(
            button_x, self.game_window.height - 570, button_width, button_height,
            "Orders", ui_batch
        )
        
        # Save Game button
        self.game_window.save_button = Button(
            button_x, self.game_window.height - 610, button_width, button_height,
            "Save Game", ui_batch
        )
        
        # Load Game button
        self.game_window.load_button = Button(
            button_x, self.game_window.height - 650, button_width, button_height,
            "Load Game", ui_batch
        )
    
    def reset_all_buttons(self):
        """Reset all button states"""
        self.game_window.tractor_button.set_pressed(False)
        self.game_window.buy_tiles_button.set_pressed(False)
        self.game_window.plant_seeds_button.set_pressed(False)
        self.game_window.harvest_button.set_pressed(False)
        self.game_window.build_button.set_pressed(False)
        self.game_window.cultivate_button.set_pressed(False)
        self.game_window.cultivator_button.set_pressed(False)
        self.game_window.upgrade_tractor_button.set_pressed(False)
        self.game_window.market_history_button.set_pressed(False)
        self.game_window.live_market_button.set_pressed(False)
        self.game_window.overlays_button.set_pressed(False)
        self.game_window.fertilizer_info_button.set_pressed(False)
        self.game_window.financial_button.set_pressed(False)
        self.game_window.orders_button.set_pressed(False)
        self.game_window.save_button.set_pressed(False)
        self.game_window.load_button.set_pressed(False)
        # Row mode toggle is not a toggle button, so no reset needed
        # Reset seed bin selection
        self.game_window.game_state.selected_seed = None
        self.game_window.popup_system.selected_seed_bin = None
    
    def set_mode(self, mode, button=None):
        """Set a specific mode, always resetting other buttons first"""
        from constants import MOUSE_MODE_TRACTOR, MOUSE_MODE_PLANT_SEEDS, MOUSE_MODE_CULTIVATE, MOUSE_MODE_HARVEST, MOUSE_MODE_CULTIVATOR, MOUSE_MODE_NORMAL
        
        # Store selected seed temporarily if switching to plant seeds mode
        temp_selected_seed = None
        temp_selected_seed_bin = None
        if mode == MOUSE_MODE_PLANT_SEEDS:
            temp_selected_seed = self.game_window.game_state.selected_seed
            temp_selected_seed_bin = self.game_window.popup_system.selected_seed_bin
        
        # Always reset all buttons first
        self.reset_all_buttons()
        
        # Restore seed selection if we're switching to plant seeds mode
        if mode == MOUSE_MODE_PLANT_SEEDS and temp_selected_seed:
            self.game_window.game_state.selected_seed = temp_selected_seed
            self.game_window.popup_system.selected_seed_bin = temp_selected_seed_bin
        
        # Set the new mode
        self.game_window.mouse_mode = mode
        
        # Set the appropriate button as pressed
        if button:
            button.set_pressed(True)
        
        # Set appropriate cursor
        if mode == MOUSE_MODE_NORMAL:
            self.game_window.set_mouse_cursor(None)
        else:
            # Use custom tractor cursor for all tractor-related farming actions
            tractor_modes = [MOUSE_MODE_TRACTOR, MOUSE_MODE_PLANT_SEEDS, MOUSE_MODE_CULTIVATE, MOUSE_MODE_HARVEST, MOUSE_MODE_CULTIVATOR]
            if mode in tractor_modes and hasattr(self.game_window, 'tractor_cursor'):
                self.game_window.set_mouse_cursor(self.game_window.tractor_cursor)
            else:
                # Default cursors for different modes
                if mode == MOUSE_MODE_BUY_TILES:
                    cursor = pyglet.window.Window.CURSOR_HAND
                elif mode == MOUSE_MODE_BUILD:
                    cursor = pyglet.window.Window.CURSOR_CROSSHAIR
                else:
                    cursor = pyglet.window.Window.CURSOR_CROSSHAIR
                self.game_window.set_mouse_cursor(self.game_window.get_system_mouse_cursor(cursor))
    
    def toggle_mode(self, mode, button, cursor):
        """Toggle between normal mode and specified mode"""
        from constants import MOUSE_MODE_TRACTOR, MOUSE_MODE_PLANT_SEEDS, MOUSE_MODE_CULTIVATE, MOUSE_MODE_HARVEST, MOUSE_MODE_CULTIVATOR
        
        # Check if we're clicking the same button that's already pressed
        if self.game_window.mouse_mode != MOUSE_MODE_NORMAL and button.pressed:
            # Clicking the same active button - switch to normal mode
            self.game_window.mouse_mode = MOUSE_MODE_NORMAL
            self.reset_all_buttons()
            self.game_window.set_mouse_cursor(None)
        else:
            # Switching to a new tool mode (either from normal or from another tool)
            # Always reset all buttons first, then set the new tool mode
            self.reset_all_buttons()
            self.game_window.mouse_mode = mode
            button.set_pressed(True)
            
            # Use custom tractor cursor for all tractor-related farming actions
            tractor_modes = [MOUSE_MODE_TRACTOR, MOUSE_MODE_PLANT_SEEDS, MOUSE_MODE_CULTIVATE, MOUSE_MODE_HARVEST, MOUSE_MODE_CULTIVATOR]
            if mode in tractor_modes and hasattr(self.game_window, 'tractor_cursor'):
                self.game_window.set_mouse_cursor(self.game_window.tractor_cursor)
            else:
                self.game_window.set_mouse_cursor(self.game_window.get_system_mouse_cursor(cursor))
    
    def draw_ui_info(self):
        """UI info is now displayed in a separate window"""
        pass
    
    def update_row_mode_button(self):
        """Update row mode toggle button visibility and text"""
        is_3_row_purchased = getattr(self.game_window.game_state, 'tractor_3_row_purchased', False)
        current_mode = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
        
        # Show button only if 3-row upgrade is purchased
        self.game_window.row_mode_toggle_button.visible = is_3_row_purchased
        
        if is_3_row_purchased:
            # Update button text to simple label
            self.game_window.row_mode_toggle_button.text = "Toggle Row Mode"
                
    def toggle_row_mode(self):
        """Toggle between 1 row and 3 row mode"""
        is_3_row_purchased = getattr(self.game_window.game_state, 'tractor_3_row_purchased', False)
        if not is_3_row_purchased:
            return  # Can't toggle if upgrade not purchased
            
        current_mode = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
        if current_mode == 1:
            self.game_window.game_state.tractor_row_mode = 3
            print("Switched to 3 Row Mode - tractors will work on 3 rows at once!")
        else:
            self.game_window.game_state.tractor_row_mode = 1
            print("Switched to 1 Row Mode - tractors will work on single rows.")
            
        self.update_row_mode_button()
    
    def toggle_financial_window(self):
        """Toggle the financial summary window"""
        if self.financial_window.is_visible():
            self.financial_window.hide()
        else:
            self.financial_window.show()

    def draw_row_mode_indicator(self):
        """Draw row mode indicator under the row mode button"""
        if not self.game_window.row_mode_toggle_button.visible:
            return  # Don't show indicator if button is hidden
            
        current_mode = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
        mode_text = f"{current_mode} Row Mode"
        
        # Position 10 pixels from the bottom of the screen
        pyglet.text.Label(
            mode_text,
            font_name='Arial',
            font_size=12,
            x=self.game_window.row_mode_toggle_button.x + self.game_window.row_mode_toggle_button.width // 2,
            y=10,
            anchor_x='center',
            anchor_y='bottom',
            color=(255, 255, 255, 255)
        ).draw()

    def draw_queue_status(self):
        """Draw tractor job queue status in bottom right area"""
        # Queue status removed per user request
        pass

    def draw_mode_indicators(self):
        """Draw cursor indicators for different modes at bottom of screen"""
        # All mode indicator notifications removed per user request
        pass
    
    def update_button_positions(self):
        """Update button positions when window is resized"""
        # Recalculate button_x based on new window width
        button_x = self.game_window.width - 225  # 10 pixels from right edge
        button_width = 215
        button_height = 35
        
        # Update all button positions
        if hasattr(self.game_window, 'buy_tiles_button'):
            self.game_window.buy_tiles_button.x = button_x
        if hasattr(self.game_window, 'build_button'):
            self.game_window.build_button.x = button_x
        if hasattr(self.game_window, 'upgrade_tractor_button'):
            self.game_window.upgrade_tractor_button.x = button_x
        if hasattr(self.game_window, 'market_history_button'):
            self.game_window.market_history_button.x = button_x
        if hasattr(self.game_window, 'live_market_button'):
            self.game_window.live_market_button.x = button_x
        if hasattr(self.game_window, 'overlays_button'):
            self.game_window.overlays_button.x = button_x
        if hasattr(self.game_window, 'fertilizer_info_button'):
            self.game_window.fertilizer_info_button.x = button_x
        if hasattr(self.game_window, 'row_mode_toggle_button'):
            self.game_window.row_mode_toggle_button.x = button_x
        if hasattr(self.game_window, 'financial_button'):
            self.game_window.financial_button.x = button_x

