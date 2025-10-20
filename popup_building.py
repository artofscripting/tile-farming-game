from constants import BUILDING_BARN, BUILDING_SEED_BIN, MOUSE_MODE_BUILD
import pyglet


class PopupBuilding:
    """Handles building selection popups"""
    
    def __init__(self, popup_core):
        self.core = popup_core
    
    def show_building_selection_popup(self):
        """Show popup to select building type"""
        self.core.show_building_popup = True
        self.core.show_seed_type_popup = False
        self.core.popup_buttons = []
        
        # Create popup buttons for building selection
        popup_x = self.core.game_window.width // 2 - 100
        popup_y = self.core.game_window.height // 2
        
        self.core.popup_buttons.append({
            'text': 'Build Barn',
            'x': popup_x, 'y': popup_y + 30,
            'width': 200, 'height': 40,
            'action': 'build_barn'
        })
        
        self.core.popup_buttons.append({
            'text': 'Build Seed Bin',
            'x': popup_x, 'y': popup_y - 20,
            'width': 200, 'height': 40,
            'action': 'build_seed_bin'
        })
        
        self.core.popup_buttons.append({
            'text': 'Cancel',
            'x': popup_x, 'y': popup_y - 70,
            'width': 200, 'height': 40,
            'action': 'cancel'
        })
    
    def handle_building_action(self, action):
        """Handle building-related actions"""
        if action == 'build_barn':
            self.core.game_window.selected_building = BUILDING_BARN
            self.core.selected_seed_type = None
            self.core.close_popups()
            self.core.game_window.ui_manager.set_mode(MOUSE_MODE_BUILD, self.core.game_window.build_button)
            return True
        elif action == 'build_seed_bin':
            # Delegate to seeds popup
            return False  # Let seeds handler take over
        return False

