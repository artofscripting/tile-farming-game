"""
Main input handler - coordinates all input handling components
"""
from input_keyboard_handler import KeyboardHandler
from input_mouse_handler import MouseHandler


class InputHandler:
    """Main input handler that coordinates all input processing"""
    
    def __init__(self, game_window):
        self.game_window = game_window
        
        # Initialize sub-handlers
        self.keyboard_handler = KeyboardHandler(game_window)
        self.mouse_handler = MouseHandler(game_window)
    
    def handle_key_press(self, symbol, modifiers):
        """Handle keyboard input"""
        self.keyboard_handler.handle_key_press(symbol, modifiers)
    
    def handle_mouse_press(self, x, y, button, modifiers):
        """Handle mouse button presses"""
        self.mouse_handler.handle_mouse_press(x, y, button, modifiers)

