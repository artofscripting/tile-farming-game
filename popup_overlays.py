import pyglet
from constants import (
    OVERLAY_NONE, OVERLAY_WEEDS, OVERLAY_WATER, OVERLAY_NITROGEN,
    OVERLAY_PHOSPHORUS, OVERLAY_POTASSIUM, OVERLAY_CALCIUM,
    OVERLAY_MAGNESIUM, OVERLAY_SULFUR, OVERLAY_SEED_REQUIREMENTS, seeds_config
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
            ("Sulfur", OVERLAY_SULFUR),
            ("Seed Requirements", OVERLAY_SEED_REQUIREMENTS)
        ]
    
    def show_overlay_selection_popup(self):
        """Show popup to select overlay type"""
        # Close any existing popups first
        self.core.close_popups()
        
        # Set popup state
        self.core.show_overlay_popup = True
        
        # Create overlay selection buttons with scrolling
        self.core.overlay_buttons = []
        popup_x = self.game_window.width // 2 - 175  # Centered for 350px buttons in 400px popup
        popup_y = self.game_window.height // 2 + 115  # Adjusted for taller popup, moved down 60px total
        button_height = 35  # Slightly taller buttons
        button_spacing = 40   # More spacing between buttons
        
        # Calculate visible range
        start_idx = self.core.overlay_scroll_offset
        end_idx = min(start_idx + self.core.overlay_items_per_page, len(self.overlay_options))
        
        # Create buttons for visible overlay options
        for i, option_idx in enumerate(range(start_idx, end_idx)):
            name, overlay_type = self.overlay_options[option_idx]
            self.core.overlay_buttons.append({
                'text': name,
                'x': popup_x, 'y': popup_y - (i * button_spacing),
                'width': 350, 'height': button_height,
                'overlay_type': overlay_type
            })
        
        return True
    
    def _update_overlay_buttons(self):
        """Update overlay popup buttons based on current scroll offset"""
        # Create overlay selection buttons with scrolling
        self.core.overlay_buttons = []
        popup_x = self.game_window.width // 2 - 175  # Centered for 350px buttons in 400px popup
        popup_y = self.game_window.height // 2 + 115  # Adjusted for taller popup, moved down 60px total
        button_height = 35  # Slightly taller buttons
        button_spacing = 40   # More spacing between buttons
        
        # Calculate visible range
        start_idx = self.core.overlay_scroll_offset
        end_idx = min(start_idx + self.core.overlay_items_per_page, len(self.overlay_options))
        
        # Create buttons for visible overlay options
        for i, option_idx in enumerate(range(start_idx, end_idx)):
            name, overlay_type = self.overlay_options[option_idx]
            self.core.overlay_buttons.append({
                'text': name,
                'x': popup_x, 'y': popup_y - (i * button_spacing),
                'width': 350, 'height': button_height,
                'overlay_type': overlay_type
            })
    
    def handle_overlay_button_click(self, x, y):
        """Handle clicks on overlay selection buttons"""
        if not hasattr(self.core, 'overlay_buttons'):
            return False
            
        for button in self.core.overlay_buttons:
            # Check if click is within button bounds
            if (button['x'] <= x <= button['x'] + button['width'] and
                button['y'] <= y <= button['y'] + button['height']):
                # Set the selected overlay
                overlay_type = button.get('overlay_type', OVERLAY_NONE)
                
                # If seed requirements overlay, show seed selection popup
                if overlay_type == OVERLAY_SEED_REQUIREMENTS:
                    self.show_seed_selection_popup()
                else:
                    self.game_window.overlay_manager.set_overlay(overlay_type)
                    # Close the popup
                    self.core.close_popups()
                
                return True
        
        return False
    
    def show_seed_selection_popup(self):
        """Show popup to select seed type for requirements overlay"""
        # Close existing overlay buttons
        self.core.close_popups()
        
        # Set popup state for seed selection
        self.core.show_seed_popup = True
        
        # Initialize seed scroll attributes
        if not hasattr(self.core, 'seed_scroll_offset'):
            self.core.seed_scroll_offset = 0
        if not hasattr(self.core, 'seed_items_per_page'):
            self.core.seed_items_per_page = 8  # Show 8 seeds per page
        
        # Create seed selection buttons with scrolling
        self.core.seed_buttons = []
        popup_x = self.game_window.width // 2 - 175  # Centered for 350px buttons in 400px popup
        popup_y = self.game_window.height // 2 + 115  # Start position for first button, centered to match overlay popup
        button_height = 35
        button_spacing = 40
        
        # Get seed types from config with scrolling
        seed_types = [seed["name"] for seed in seeds_config]
        start_idx = self.core.seed_scroll_offset
        end_idx = min(start_idx + self.core.seed_items_per_page, len(seed_types))
        

        
        # Create buttons for visible seed types only (using range for visible items)
        for i, seed_idx in enumerate(range(start_idx, end_idx)):
            seed_type = seed_types[seed_idx]
            from button import Button
            # Position buttons based on their visible index (i), not their absolute index
            button_y = popup_y - (i * button_spacing)

            button = Button(
                popup_x, button_y, 350, button_height,
                seed_type, self.core.popup_batch
            )
            button.seed_type = seed_type  # Store seed type in button
            self.core.seed_buttons.append(button)

    
    def handle_seed_button_click(self, x, y):
        """Handle clicks on seed selection buttons"""
        if not hasattr(self.core, 'seed_buttons'):
            return False
            
        for button in self.core.seed_buttons:
            if button.contains_point(x, y):
                # Set the selected seed for requirements overlay
                seed_type = getattr(button, 'seed_type', None)
                if seed_type:
                    self.game_window.overlay_manager.set_seed_for_requirements(seed_type)
                    self.game_window.overlay_manager.set_overlay(OVERLAY_SEED_REQUIREMENTS)
                
                # Close the popup
                self.core.close_popups()
                
                return True
                
        return False
        
        return False

