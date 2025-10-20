"""
Button rendering for popups
"""
import pyglet


class PopupButtonRenderer:
    """Handles popup button rendering"""
    
    def __init__(self, game_window):
        self.game_window = game_window
    
    def draw_standard_buttons(self, buttons):
        """Draw standard popup buttons (used by most popup types)"""
        if not buttons:
            return
            
        for button in buttons:
            self._draw_button_dict(button)
    
    def draw_overlay_buttons(self, buttons):
        """Draw overlay popup buttons"""  
        if not buttons:
            return
            
        for button in buttons:
            self._draw_button_dict(button)
    
    def draw_seed_buttons(self, buttons):
        """Draw seed selection popup buttons"""
        if not buttons:
            return
            
        for button in buttons:
            # Check if button is a dictionary or Button object
            if isinstance(button, dict):
                self._draw_button_dict(button)
            else:
                # Assume it's a Button object with attributes
                self._draw_button_object(button)
    
    def _draw_button_dict(self, button):
        """Draw a button from a dictionary definition"""
        color = (0, 80, 0)  # Medium green button color - visible but not too bright
        
        # Button rectangle
        rect = pyglet.shapes.Rectangle(
            button['x'], button['y'], button['width'], button['height'],
            color=color, batch=None
        )
        rect.draw()
        
        # Button border
        border = pyglet.shapes.Rectangle(
            button['x'] - 1, button['y'] - 1, button['width'] + 2, button['height'] + 2,
            color=(120, 120, 120), batch=None
        )
        border.draw()
        
        # Button text
        text_label = pyglet.text.Label(
            button['text'],
            x=button['x'] + button['width'] // 2,
            y=button['y'] + button['height'] // 2,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255),
            font_size=12
        )
        text_label.draw()
    
    def _draw_button_object(self, button):
        """Draw a button from an object with attributes"""
        color = (0, 80, 0)  # Medium green button color - visible but not too bright
        
        # Button rectangle
        rect = pyglet.shapes.Rectangle(
            button.x, button.y, button.width, button.height,
            color=color, batch=None
        )
        rect.draw()
        
        # Button border
        border = pyglet.shapes.Rectangle(
            button.x - 1, button.y - 1, button.width + 2, button.height + 2,
            color=(120, 120, 120), batch=None
        )
        border.draw()
        
        # Button text
        text_label = pyglet.text.Label(
            button.text,
            x=button.x + button.width // 2,
            y=button.y + button.height // 2,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255),
            font_size=12
        )
        text_label.draw()

