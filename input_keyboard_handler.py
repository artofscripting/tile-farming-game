"""
Keyboard input handling
"""
import pyglet
from constants import OVERLAY_NONE


class KeyboardHandler:
    """Handles keyboard input events"""
    
    def __init__(self, game_window):
        self.game_window = game_window
    
    def handle_key_press(self, symbol, modifiers):
        """Handle keyboard input"""
        # Handle escape key to close overlays
        if symbol == pyglet.window.key.ESCAPE:
            if (hasattr(self.game_window, 'overlay_manager') and 
                self.game_window.overlay_manager.current_overlay != OVERLAY_NONE):
                self.game_window.overlay_manager.set_overlay(OVERLAY_NONE)
                print("Overlay closed with Escape key")
                return
        
        # Handle P key for purchasing tractors
        if symbol == pyglet.window.key.P:
            if hasattr(self.game_window, 'tractor_manager'):
                self.game_window.managers.tractor_manager.purchase_tractor()
            return
        
        # No other hotkeys - all input is handled through mouse interface
        pass

