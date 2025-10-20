from popup_core import PopupCore
from popup_building import PopupBuilding
from popup_seeds import PopupSeeds
from popup_fertilizer import PopupFertilizer
from popup_tractor import PopupTractor
from popup_overlays import PopupOverlays
from popup_renderer import PopupRenderer


class PopupSystem:
    """Main PopupSystem class that coordinates all popup functionality"""
    
    def __init__(self, game_window):
        # Initialize core popup functionality
        self.core = PopupCore(game_window)
        
        # Initialize specialized popup handlers
        self.building = PopupBuilding(self.core)
        self.seeds = PopupSeeds(self.core)
        self.fertilizer = PopupFertilizer(self.core)
        self.tractor = PopupTractor(self.core)
        self.overlays = PopupOverlays(self.core)
        self.renderer = PopupRenderer(self.core)
        
        # Expose commonly used core attributes for backward compatibility
        self.game_window = self.core.game_window
    
    # Delegate popup display methods to specialized handlers
    def show_building_selection_popup(self):
        """Show popup to select building type"""
        result = self.building.show_building_selection_popup()
        self._sync_attributes()
        return result
    
    def show_seed_type_selection_popup(self):
        """Show popup to select seed type for seed bin"""
        result = self.seeds.show_seed_type_selection_popup()
        self._sync_attributes()
        return result
    
    def show_seed_bin_selection_popup(self):
        """Show popup to select seed bin for planting"""
        result = self.seeds.show_seed_bin_selection_popup()
        self._sync_attributes()
        return result
    
    def show_seed_bin_management_popup(self, tile):
        """Show popup to manage seed bin (buy seeds/upgrade building)"""
        result = self.seeds.show_seed_bin_management_popup(tile)
        self._sync_attributes()
        return result
    
    def show_fertilizer_selection_popup(self):
        """Show popup to select fertilizer for cultivation"""
        result = self.fertilizer.show_fertilizer_selection_popup()
        self._sync_attributes()
        return result
    
    def show_tractor_upgrade_popup(self):
        """Show popup to select tractor row operation mode"""
        result = self.tractor.show_tractor_upgrade_popup()
        self._sync_attributes()
        return result
    
    def show_overlay_selection_popup(self):
        """Show popup to select overlay type"""
        result = self.overlays.show_overlay_selection_popup()
        self._sync_attributes()
        return result
    
    # Core functionality delegation
    def close_popups(self):
        """Close all popups"""
        result = self.core.close_popups()
        self._sync_attributes()
        return result
    
    def is_showing_popup(self):
        """Check if any popup is currently showing"""
        return self.core.is_showing_popup()
    
    def update_mouse_position(self, x, y):
        """Update mouse position and check for button hover"""
        result = self.core.update_mouse_position(x, y)
        self._sync_attributes()
        return result
    
    def get_seed_price(self, seed_name):
        """Get the price of a specific seed type from seeds config"""
        return self.core.get_seed_price(seed_name)
    
    # Main click handler that coordinates all popup types
    def handle_click(self, x, y):
        """Handle clicks on popup buttons"""
        if not self.core.is_showing_popup():
            return False
        
        # Handle overlay button clicks first
        if self.core.show_overlay_popup:
            if self.overlays.handle_overlay_button_click(x, y):
                self._sync_attributes()
                return True
        
        # Handle seed selection popup clicks
        if self.core.show_seed_popup:
            if self.overlays.handle_seed_button_click(x, y):
                self._sync_attributes()
                return True
            
        for button in self.core.popup_buttons:
            if (button['x'] <= x <= button['x'] + button['width'] and
                button['y'] <= y <= button['y'] + button['height']):
                
                # Try each handler in order
                if self._handle_building_actions(button['action']):
                    self._sync_attributes()
                    return True
                elif self._handle_seed_actions(button['action']):
                    self._sync_attributes()
                    return True
                elif self._handle_fertilizer_actions(button['action']):
                    self._sync_attributes()
                    return True
                elif self._handle_tractor_actions(button['action']):
                    self._sync_attributes()
                    return True
                elif button['action'] == 'cancel':
                    self.core.pending_seed_purchase = None  # Clear pending purchase
                    self.core.close_popups()
                    self._sync_attributes()
                    return True
                
        return False
    
    def _handle_building_actions(self, action):
        """Handle building-related actions"""
        if action == 'build_barn':
            return self.building.handle_building_action(action)
        elif action == 'build_seed_bin':
            self.seeds.show_seed_type_selection_popup()
            return True
        return False
    
    def _handle_seed_actions(self, action):
        """Handle seed-related actions"""
        if action.startswith('select_seed_') or action.startswith('select_bin_') or action.startswith('manage_'):
            return self.seeds.handle_seed_action(action)
        return False
    
    def _handle_fertilizer_actions(self, action):
        """Handle fertilizer-related actions"""
        if action.startswith('select_fertilizer_'):
            return self.fertilizer.handle_fertilizer_action(action)
        return False
    
    def _handle_tractor_actions(self, action):
        """Handle tractor-related actions"""
        if (action.startswith('set_tractor_') or 
            action == 'buy_tractor_3_row' or 
            action == 'buy_tractor_speed' or 
            action == 'buy_additional_tractor' or 
            action == 'speed_info'):
            return self.tractor.handle_tractor_action(action)
        return False
    
    # Drawing delegation
    def draw(self):
        """Draw popups if they're showing"""
        self.renderer.draw()
    
    # Synchronize attributes for backward compatibility
    def _sync_attributes(self):
        """Sync core attributes to main object for backward compatibility"""
        self.show_building_popup = self.core.show_building_popup
        self.show_seed_type_popup = self.core.show_seed_type_popup
        self.show_seed_bin_popup = self.core.show_seed_bin_popup
        self.show_fertilizer_popup = self.core.show_fertilizer_popup
        self.show_tractor_upgrade = self.core.show_tractor_upgrade
        self.show_overlay_popup = self.core.show_overlay_popup
        self.show_seed_bin_management = self.core.show_seed_bin_management
        self.popup_buttons = self.core.popup_buttons
        self.overlay_buttons = self.core.overlay_buttons
        self.selected_seed_type = self.core.selected_seed_type
        self.selected_seed_bin = self.core.selected_seed_bin
        self.pending_seed_purchase = self.core.pending_seed_purchase
        self.selected_fertilizer = self.core.selected_fertilizer
        self.hovered_button = self.core.hovered_button
        self.managed_seed_bin_tile = self.core.managed_seed_bin_tile
        
        # Additional attributes that might be accessed
        self.mouse_x = self.core.mouse_x
        self.mouse_y = self.core.mouse_y
        self.seed_type_scroll_offset = self.core.seed_type_scroll_offset
        self.seed_type_items_per_page = self.core.seed_type_items_per_page
        self.fertilizer_scroll_offset = self.core.fertilizer_scroll_offset
        self.fertilizer_items_per_page = self.core.fertilizer_items_per_page
        self.fertilizer_config = self.core.fertilizer_config

