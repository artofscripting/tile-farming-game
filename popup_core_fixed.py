import pyglet


class PopupCore:
    """Core popup functionality and state management"""
    
    def __init__(self, game_window):
        self.game_window = game_window
        
        # Popup state flags
        self.show_building_popup = False
        self.show_seed_type_popup = False
        self.show_seed_bin_popup = False
        self.show_fertilizer_popup = False
        self.show_tractor_upgrade = False
        self.show_overlay_popup = False
        
        # Common popup data
        self.popup_buttons = []
        self.overlay_buttons = []
        self.popup_batch = pyglet.graphics.Batch()
        
        # Building popup data
        self.building_options = [
            ("Barn", "barn"),
            ("Seed Bin", "seed_bin")
        ]
        
        # Seed type popup scrolling
        self.seed_type_scroll_offset = 0
        self.seed_type_items_per_page = 9
        
        # Seed bin popup data
        self.seed_bin_options = []
        
        # Fertilizer popup scrolling
        self.fertilizer_config = []
        self.fertilizer_scroll_offset = 0
        self.fertilizer_items_per_page = 8
        
        # Tractor upgrade data
        self.tractor_upgrades = []
        
        # Popup tooltip data
        self.popup_tooltip_text = ""
        self.popup_tooltip_x = 0
        self.popup_tooltip_y = 0
        
    def close_popups(self):
        """Close all popups"""
        self.show_building_popup = False
        self.show_seed_type_popup = False
        self.show_seed_bin_popup = False
        self.show_fertilizer_popup = False
        self.show_tractor_upgrade = False
        self.show_overlay_popup = False
        self.popup_buttons = []
        self.overlay_buttons = []
    
    def is_showing_popup(self):
        """Check if any popup is currently showing"""
        return (self.show_building_popup or self.show_seed_type_popup or 
                self.show_seed_bin_popup or self.show_fertilizer_popup or 
                self.show_tractor_upgrade or self.show_overlay_popup)
    
    def get_popup_tooltip(self):
        """Get current popup tooltip text and position"""
        return self.popup_tooltip_text, self.popup_tooltip_x, self.popup_tooltip_y
    
    def set_popup_tooltip(self, text, x, y):
        """Set popup tooltip text and position"""
        self.popup_tooltip_text = text
        self.popup_tooltip_x = x
        self.popup_tooltip_y = y
    
    def clear_popup_tooltip(self):
        """Clear popup tooltip"""
        self.popup_tooltip_text = ""
    
    def update_mouse_position(self, x, y):
        """Update mouse position for popup interactions"""
        # Check if mouse is over any popup elements and update tooltip
        if self.is_showing_popup():
            self.clear_popup_tooltip()
            
            # Check overlay buttons for tooltips
            if self.show_overlay_popup and hasattr(self, 'overlay_buttons'):
                for button in self.overlay_buttons:
                    if hasattr(button, 'contains_point') and button.contains_point(x, y):
                        overlay_type = getattr(button, 'overlay_type', None)
                        if overlay_type is not None:
                            self.set_popup_tooltip(f"Select {button.text} overlay", x, y)
                            break

