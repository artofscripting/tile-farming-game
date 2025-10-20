"""
Main popup renderer - coordinates all popup rendering components
"""
import pyglet
from constants import seeds_config
from popup_background_renderer import PopupBackgroundRenderer
from popup_button_renderer import PopupButtonRenderer
from popup_scroll_renderer import PopupScrollRenderer
from popup_tooltip_renderer import PopupTooltipRenderer


class PopupRenderer:
    """Main popup renderer that coordinates all popup rendering"""
    
    def __init__(self, popup_core):
        self.core = popup_core
        
        # Initialize sub-renderers
        self.background_renderer = PopupBackgroundRenderer(popup_core.game_window)
        self.button_renderer = PopupButtonRenderer(popup_core.game_window)
        self.scroll_renderer = PopupScrollRenderer(popup_core.game_window)
        self.tooltip_renderer = PopupTooltipRenderer(popup_core.game_window)
    
    def draw(self):
        """Draw popups if they're showing"""
        if self.core.show_building_popup:
            self.draw_building_selection_popup()
        elif self.core.show_seed_type_popup:
            self.draw_seed_type_selection_popup()
        elif self.core.show_seed_bin_popup:
            self.draw_seed_bin_selection_popup()
        elif self.core.show_fertilizer_popup:
            self.draw_fertilizer_selection_popup()
        elif self.core.show_tractor_upgrade:
            self.draw_tractor_upgrade_popup()
        elif self.core.show_overlay_popup:
            self.draw_overlay_selection_popup()
        elif self.core.show_seed_popup:
            self.draw_seed_selection_popup()
        elif self.core.show_seed_bin_management:
            self.draw_seed_bin_management_popup()
            
        # Draw popup tooltips on top of everything
        self.draw_popup_tooltip()
    
    def draw_building_selection_popup(self):
        """Draw the building selection popup"""
        self.background_renderer.draw_building_background("Select Building Type")
        self.button_renderer.draw_standard_buttons(getattr(self.core, 'popup_buttons', []))
    
    def draw_seed_type_selection_popup(self):
        """Draw the seed type selection popup"""
        title = "Select Seed Type for Seed Bin"
        
        # Add scroll info to title if there are multiple pages
        if len(seeds_config) > self.core.seed_type_items_per_page:
            current_page = (self.core.seed_type_scroll_offset // self.core.seed_type_items_per_page) + 1
            total_pages = ((len(seeds_config) - 1) // self.core.seed_type_items_per_page) + 1
            title += f" (Page {current_page}/{total_pages})"
        
        popup_bg_x, popup_bg_y, popup_width, popup_height = self.background_renderer.draw_seed_type_background(title)
        self.button_renderer.draw_standard_buttons(getattr(self.core, 'popup_buttons', []))
        
        # Draw scroll indicators for seed type popup
        if len(seeds_config) > self.core.seed_type_items_per_page:
            self.scroll_renderer.draw_seed_type_scroll_indicators(
                popup_bg_x, popup_bg_y, popup_width, popup_height,
                self.core.seed_type_scroll_offset, self.core.seed_type_items_per_page
            )
    
    def draw_seed_bin_selection_popup(self):
        """Draw the seed bin selection popup"""
        self.background_renderer.draw_seed_bin_background("Select Seeds for Planting")
        self.button_renderer.draw_standard_buttons(getattr(self.core, 'popup_buttons', []))
    
    def draw_fertilizer_selection_popup(self):
        """Draw the fertilizer selection popup"""
        title = "Fertilizing"
        
        # Add scroll info to title if there are multiple pages
        if len(self.core.fertilizer_config) > self.core.fertilizer_items_per_page:
            current_page = (self.core.fertilizer_scroll_offset // self.core.fertilizer_items_per_page) + 1
            total_pages = ((len(self.core.fertilizer_config) - 1) // self.core.fertilizer_items_per_page) + 1
            title += f" (Page {current_page}/{total_pages})"
        
        popup_bg_x, popup_bg_y, popup_width, popup_height = self.background_renderer.draw_fertilizer_background(title)
        self.button_renderer.draw_standard_buttons(getattr(self.core, 'popup_buttons', []))
        
        # Draw scroll indicators
        if len(self.core.fertilizer_config) > self.core.fertilizer_items_per_page:
            self.scroll_renderer.draw_fertilizer_scroll_indicators(
                popup_bg_x, popup_bg_y, popup_width, popup_height,
                self.core.fertilizer_scroll_offset, self.core.fertilizer_items_per_page,
                self.core.fertilizer_config
            )
    
    def draw_tractor_upgrade_popup(self):
        """Draw the tractor upgrade selection popup"""
        self.background_renderer.draw_tractor_upgrade_background("Tractor Upgrades")
        self.button_renderer.draw_standard_buttons(getattr(self.core, 'popup_buttons', []))
    
    def draw_overlay_selection_popup(self):
        """Draw the overlay selection popup"""
        title = "Select Overlay Type"
        
        # Get overlay options count
        overlay_options_count = 10  # We know there are 10 overlay options
        
        # Add scroll info to title if there are multiple pages
        if overlay_options_count > self.core.overlay_items_per_page:
            current_page = (self.core.overlay_scroll_offset // self.core.overlay_items_per_page) + 1
            total_pages = ((overlay_options_count - 1) // self.core.overlay_items_per_page) + 1
            title += f" (Page {current_page}/{total_pages})"
        
        popup_bg_x, popup_bg_y, popup_width, popup_height = self.background_renderer.draw_overlay_background(title)
        self.button_renderer.draw_overlay_buttons(getattr(self.core, 'overlay_buttons', []))
        
        # Draw scroll indicators
        if overlay_options_count > self.core.overlay_items_per_page:
            self.scroll_renderer.draw_overlay_scroll_indicators(
                popup_bg_x, popup_bg_y, popup_width, popup_height,
                self.core.overlay_scroll_offset, self.core.overlay_items_per_page
            )
    
    def draw_seed_selection_popup(self):
        """Draw the seed selection popup"""
        title = "Select Seed Type"
        
        # Add scroll info to title if there are multiple pages
        seed_items_per_page = getattr(self.core, 'seed_items_per_page', 8)
        if len(seeds_config) > seed_items_per_page:
            seed_scroll_offset = getattr(self.core, 'seed_scroll_offset', 0)
            current_page = (seed_scroll_offset // seed_items_per_page) + 1
            total_pages = ((len(seeds_config) - 1) // seed_items_per_page) + 1
            title += f" (Page {current_page}/{total_pages})"
        
        popup_bg_x, popup_bg_y, popup_width, popup_height = self.background_renderer.draw_seed_selection_background(title)
        self.button_renderer.draw_seed_buttons(getattr(self.core, 'seed_buttons', []))
        
        # Draw scroll indicators
        if len(seeds_config) > seed_items_per_page:
            seed_scroll_offset = getattr(self.core, 'seed_scroll_offset', 0)
            self.scroll_renderer.draw_seed_scroll_indicators(
                popup_bg_x, popup_bg_y, popup_width, popup_height,
                seed_scroll_offset, seed_items_per_page
            )
    
    def draw_seed_bin_management_popup(self):
        """Draw the seed bin management popup"""
        self.background_renderer.draw_seed_bin_management_background("Manage Seed Bin")
        self.button_renderer.draw_standard_buttons(getattr(self.core, 'popup_buttons', []))
    
    def draw_popup_tooltip(self):
        """Draw popup tooltip if available"""
        tooltip_text, tooltip_x, tooltip_y = self.core.get_popup_tooltip()
        self.tooltip_renderer.draw_tooltip(tooltip_text, tooltip_x, tooltip_y)

