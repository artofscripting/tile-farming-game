from constants import MOUSE_MODE_CULTIVATE
import json
import pyglet


class PopupFertilizer:
    """Handles fertilizer selection popup"""
    
    def __init__(self, popup_core):
        self.core = popup_core
    
    def show_fertilizer_selection_popup(self):
        """Show popup to select fertilizer for cultivation"""
        self.core.show_building_popup = False
        self.core.show_seed_type_popup = False
        self.core.show_seed_bin_popup = False
        self.core.show_fertilizer_popup = True
        self.core.fertilizer_scroll_offset = 0  # Reset scroll
        self.core.popup_buttons = []
        
        # Load fertilizer config
        try:
            with open('config/fertilizer.json', 'r') as f:
                self.core.fertilizer_config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading fertilizer config: {e}")
            self.core.fertilizer_config = []
        
        self._update_fertilizer_buttons()
    
    def _update_fertilizer_buttons(self):
        """Update fertilizer popup buttons based on current scroll offset"""
        self.core.popup_buttons = []
        
        # Calculate popup background dimensions (same as in draw_popup_background)
        popup_width = 500  # Increased to accommodate wider buttons
        popup_height = 400
        popup_bg_x = self.core.game_window.width // 2 - popup_width // 2
        popup_bg_y = self.core.game_window.height // 2 - popup_height // 2
        
        # Position buttons relative to popup background, leaving space for title
        popup_x = popup_bg_x + 50  # Center buttons in popup with some margin
        popup_y = popup_bg_y + popup_height - 110  # Start below title (110px from top, moved up 20px)
        
        # Calculate visible range
        start_idx = self.core.fertilizer_scroll_offset
        end_idx = min(start_idx + self.core.fertilizer_items_per_page, len(self.core.fertilizer_config))
        
        # Create buttons for visible fertilizers
        for i, fertilizer_idx in enumerate(range(start_idx, end_idx)):
            fertilizer = self.core.fertilizer_config[fertilizer_idx]
            
            # Simple fertilizer description (nutrients will be shown in tooltip)
            description = f'{fertilizer["name"]} (${fertilizer["cost"]})'
            
            self.core.popup_buttons.append({
                'text': description,
                'x': popup_x, 'y': popup_y - i * 50,
                'width': 400, 'height': 45,  # Increased width for larger popup
                'action': f'select_fertilizer_{fertilizer["name"]}',
                'fertilizer_data': fertilizer
            })
        
        # Cancel button at bottom of popup, positioned below all fertilizer buttons
        # Calculate position based on the actual number of items shown on this page
        items_on_page = end_idx - start_idx
        lowest_button_y = popup_y - (items_on_page - 1) * 50
        cancel_y = lowest_button_y - 60  # 60px below the lowest fertilizer button
        self.core.popup_buttons.append({
            'text': 'Cancel',
            'x': popup_x, 'y': cancel_y,
            'width': 400, 'height': 45,  # Match fertilizer button width
            'action': 'cancel'
        })
    
    def handle_fertilizer_action(self, action):
        """Handle fertilizer-related actions"""
        if action.startswith('select_fertilizer_'):
            fertilizer_name = action.replace('select_fertilizer_', '')
            
            # Find the button with fertilizer data
            for button in self.core.popup_buttons:
                if button['action'] == action and 'fertilizer_data' in button:
                    self.core.selected_fertilizer = button['fertilizer_data']
                    self.core.game_window.game_state.selected_fertilizer = button['fertilizer_data']
                    
                    # Check if player can afford the fertilizer
                    fertilizer_cost = button['fertilizer_data']['cost']
                    if self.core.game_window.game_state.can_afford(fertilizer_cost):
                        self.core.close_popups()
                        self.core.game_window.ui_manager.set_mode(MOUSE_MODE_CULTIVATE, self.core.game_window.cultivate_button)
                        print(f"Selected {fertilizer_name} fertilizer for cultivation (${fertilizer_cost})")
                        print(f"Click on a farm tile to cultivate the row with fertilizer")
                    else:
                        print(f"Cannot afford {fertilizer_name} fertilizer (${fertilizer_cost})")
                        self.core.close_popups()
                    return True
            
            print(f"Error: Fertilizer data not found")
            self.core.close_popups()
            return True
            
        return False

