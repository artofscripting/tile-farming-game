import pyglet
from constants import seeds_config


class PopupRenderer:
    """Handles all popup drawing and rendering"""
    
    def __init__(self, popup_core):
        self.core = popup_core
    
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
            
        # Draw popup tooltips on top of everything
        self.draw_popup_tooltip()
    
    def draw_building_selection_popup(self):
        """Draw the building selection popup"""
        self.draw_popup_background("Select Building Type")
        self.draw_popup_buttons()
    
    def draw_seed_type_selection_popup(self):
        """Draw the seed type selection popup"""
        title = "Select Seed Type for Seed Bin"
        
        # Add scroll info to title if there are multiple pages
        if len(seeds_config) > self.core.seed_type_items_per_page:
            current_page = (self.core.seed_type_scroll_offset // self.core.seed_type_items_per_page) + 1
            total_pages = ((len(seeds_config) - 1) // self.core.seed_type_items_per_page) + 1
            title += f" (Page {current_page}/{total_pages})"
        
        self.draw_popup_background(title)
        self.draw_popup_buttons()
        
        # Draw scroll indicators for seed type popup
        if len(seeds_config) > self.core.seed_type_items_per_page:
            self._draw_seed_type_scroll_indicators()
    
    def _draw_seed_type_scroll_indicators(self):
        """Draw scroll indicators for seed type popup"""
        # Use same popup dimensions as buttons
        popup_width = 300
        popup_height = 350
        popup_bg_x = self.core.game_window.width // 2 - popup_width // 2
        popup_bg_y = self.core.game_window.height // 2 - popup_height // 2
        
        # Position scroll bar on the right side of the popup
        scrollbar_x = popup_bg_x + popup_width - 30  # 30px from right edge
        scrollbar_y = popup_bg_y + 60  # Start below title area
        scrollbar_height = popup_height - 120  # Leave space for title and cancel button
        
        # Scroll bar background
        scrollbar_bg = pyglet.shapes.Rectangle(
            scrollbar_x, scrollbar_y, 20, scrollbar_height,
            color=(40, 40, 40), batch=None
        )
        scrollbar_bg.draw()
        
        # Scroll position indicator
        total_items = len(seeds_config)
        visible_ratio = self.core.seed_type_items_per_page / total_items
        scroll_ratio = self.core.seed_type_scroll_offset / (total_items - self.core.seed_type_items_per_page)
        
        indicator_height = max(20, scrollbar_height * visible_ratio)
        indicator_y = scrollbar_y + (scrollbar_height - indicator_height) * scroll_ratio
        
        scroll_indicator = pyglet.shapes.Rectangle(
            scrollbar_x + 2, indicator_y, 16, indicator_height,
            color=(100, 100, 100), batch=None
        )
        scroll_indicator.draw()
    
    def draw_seed_bin_selection_popup(self):
        """Draw the seed bin selection popup"""
        self.draw_popup_background("Select Seeds for Planting")
        self.draw_popup_buttons()
    
    def draw_fertilizer_selection_popup(self):
        """Draw the fertilizer selection popup"""
        title = "Select Fertilizer for Cultivation"
        
        # Add scroll info to title if there are multiple pages
        if len(self.core.fertilizer_config) > self.core.fertilizer_items_per_page:
            current_page = (self.core.fertilizer_scroll_offset // self.core.fertilizer_items_per_page) + 1
            total_pages = ((len(self.core.fertilizer_config) - 1) // self.core.fertilizer_items_per_page) + 1
            title += f" (Page {current_page}/{total_pages})"
        
        self.draw_popup_background(title)
        self.draw_popup_buttons()
        
        # Draw scroll indicators
        if len(self.core.fertilizer_config) > self.core.fertilizer_items_per_page:
            self._draw_fertilizer_scroll_indicators()
    
    def _draw_fertilizer_scroll_indicators(self):
        """Draw scroll indicators for fertilizer popup"""
        # Use same popup dimensions as buttons
        popup_width = 450
        popup_height = 320
        popup_bg_x = self.core.game_window.width // 2 - popup_width // 2
        popup_bg_y = self.core.game_window.height // 2 - popup_height // 2
        
        # Position scroll bar on the right side of the popup, inside the bounds
        scrollbar_x = popup_bg_x + popup_width - 30  # 30px from right edge (20px bar + 10px margin)
        scrollbar_y = popup_bg_y + 60  # Start below title area
        scrollbar_height = popup_height - 120  # Leave space for title and cancel button
        
        # Scroll bar background
        scrollbar_bg = pyglet.shapes.Rectangle(
            scrollbar_x, scrollbar_y, 20, scrollbar_height,
            color=(40, 40, 40), batch=None
        )
        scrollbar_bg.draw()
        
        # Scroll position indicator
        total_items = len(self.core.fertilizer_config)
        visible_ratio = self.core.fertilizer_items_per_page / total_items
        scroll_ratio = self.core.fertilizer_scroll_offset / (total_items - self.core.fertilizer_items_per_page)
        
        indicator_height = max(20, scrollbar_height * visible_ratio)
        indicator_y = scrollbar_y + (scrollbar_height - indicator_height) * scroll_ratio
        
        scroll_indicator = pyglet.shapes.Rectangle(
            scrollbar_x + 2, indicator_y, 16, indicator_height,
            color=(100, 100, 100), batch=None
        )
        scroll_indicator.draw()
    
    def draw_tractor_upgrade_popup(self):
        """Draw the tractor upgrade selection popup"""
        self.draw_popup_background("Tractor Upgrades")
        self.draw_popup_buttons()
    
    def draw_overlay_selection_popup(self):
        """Draw the overlay selection popup"""
        title = "Select Overlay Type"
        
        # Add scroll info to title if there are multiple pages
        if len(self.core.overlays.overlay_options) > self.core.overlay_items_per_page:
            current_page = (self.core.overlay_scroll_offset // self.core.overlay_items_per_page) + 1
            total_pages = ((len(self.core.overlays.overlay_options) - 1) // self.core.overlay_items_per_page) + 1
            title += f" (Page {current_page}/{total_pages})"
        
        self.draw_overlay_popup_background(title)
        self.draw_overlay_popup_buttons()
        

        
    def draw_seed_selection_popup(self):

