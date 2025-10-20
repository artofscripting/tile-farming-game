"""
Tooltip rendering for popups
"""
import pyglet


class PopupTooltipRenderer:
    """Handles popup tooltip rendering"""
    
    def __init__(self, game_window):
        self.game_window = game_window
    
    def draw_tooltip(self, tooltip_text, tooltip_x, tooltip_y):
        """Draw tooltip if text is provided"""
        if not tooltip_text:
            return
            
        # Draw tooltip background
        lines = tooltip_text.split('\n')
        line_height = 18
        padding = 8
        tooltip_width = max(len(line) * 8 for line in lines) + padding * 2
        tooltip_height = len(lines) * line_height + padding * 2
        
        # Tooltip background
        tooltip_bg = pyglet.shapes.Rectangle(
            tooltip_x, tooltip_y, tooltip_width, tooltip_height,
            color=(0, 0, 0), batch=None
        )
        tooltip_bg.draw()
        
        # Tooltip border for better visibility
        tooltip_border = pyglet.shapes.Rectangle(
            tooltip_x - 1, tooltip_y - 1, tooltip_width + 2, tooltip_height + 2,
            color=(80, 80, 80), batch=None
        )
        tooltip_border.draw()
        
        # Draw tooltip text
        for i, line in enumerate(lines):
            text_label = pyglet.text.Label(
                line,
                x=tooltip_x + padding,
                y=tooltip_y + tooltip_height - padding - (i + 1) * line_height,
                color=(255, 255, 255, 255),
                font_size=12
            )
            text_label.draw()

