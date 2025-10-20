import pyglet
from constants import (
    OVERLAY_NONE, OVERLAY_WEEDS, OVERLAY_WATER, OVERLAY_NITROGEN,
    OVERLAY_PHOSPHORUS, OVERLAY_POTASSIUM, OVERLAY_CALCIUM,
    OVERLAY_MAGNESIUM, OVERLAY_SULFUR
)


class PopupOverlays:
    """Handles overlay selection popup functionality"""
    
    def __init__(self, popup_core):
        self.core = popup_core
        self.game_window = popup_core.game_window
        
        # Overlay options
        self.overlay_options = [
            ("None", OVERLAY_NONE),
            ("Weeds", OVERLAY_WEEDS),
            ("Water", OVERLAY_WATER),
            ("Nitrogen", OVERLAY_NITROGEN),
            ("Phosphorus", OVERLAY_PHOSPHORUS),
            ("Potassium", OVERLAY_POTASSIUM),
            ("Calcium", OVERLAY_CALCIUM),
            ("Magnesium", OVERLAY_MAGNESIUM),
            ("Sulfur", OVERLAY_SULFUR)
        ]
    
    def show_overlay_selection_popup(self):
        """Show popup to select overlay type"""
        # Close any existing popups first
        self.core.close_popups()
        
        # Set popup state
        self.core.show_overlay_popup = True
        
        # Create overlay selection buttons
        self.core.overlay_buttons = []
        popup_x = self.game_window.width // 2 - 150
        popup_y = self.game_window.height // 2 + 150
        button_height = 30
        button_spacing = 35
        
        for i, (name, overlay_type) in enumerate(self.overlay_options):
            from button import Button
            button = Button(
                popup_x, popup_y - (i * button_spacing), 300, button_height,
                name, self.core.popup_batch
            )
            button.overlay_type = overlay_type  # Store overlay type in button
            self.core.overlay_buttons.append(button)
        
        return True
    
    def handle_overlay_button_click(self, x, y):
        """Handle clicks on overlay selection buttons"""
        if not hasattr(self.core, 'overlay_buttons'):
            return False
            
        for button in self.core.overlay_buttons:
            if button.contains_point(x, y):
                # Set the selected overlay
                overlay_type = getattr(button, 'overlay_type', OVERLAY_NONE)
                self.game_window.overlay_manager.set_overlay(overlay_type)
                
                # Close the popup
                self.core.close_popups()
                
                return True
        
        return False

