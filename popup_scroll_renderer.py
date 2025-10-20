"""
Scroll indicator rendering for popups
"""
import pyglet
from constants import seeds_config


class PopupScrollRenderer:
    """Handles popup scroll indicator rendering"""
    
    def __init__(self, game_window):
        self.game_window = game_window
    
    def draw_seed_type_scroll_indicators(self, popup_bg_x, popup_bg_y, popup_width, popup_height, 
                                       scroll_offset, items_per_page):
        """Draw scroll indicators for seed type popup"""
        # Position scroll bar on the right side of the popup
        scrollbar_x = popup_bg_x + popup_width - 30  # 30px from right edge
        scrollbar_y = popup_bg_y + 70  # Start below title area with more space
        scrollbar_height = popup_height - 140  # Leave space for title and cancel button
        
        self._draw_scrollbar(scrollbar_x, scrollbar_y, scrollbar_height, 
                           len(seeds_config), items_per_page, scroll_offset)
    
    def draw_fertilizer_scroll_indicators(self, popup_bg_x, popup_bg_y, popup_width, popup_height,
                                        scroll_offset, items_per_page, fertilizer_config):
        """Draw scroll indicators for fertilizer popup"""
        # Position scroll bar on the right side of the popup, inside the bounds
        scrollbar_x = popup_bg_x + popup_width - 30  # 30px from right edge
        scrollbar_y = popup_bg_y + 60  # Start below title area
        scrollbar_height = popup_height - 120  # Leave space for title and cancel button
        
        self._draw_scrollbar(scrollbar_x, scrollbar_y, scrollbar_height,
                           len(fertilizer_config), items_per_page, scroll_offset)
    
    def draw_overlay_scroll_indicators(self, popup_bg_x, popup_bg_y, popup_width, popup_height,
                                     scroll_offset, items_per_page):
        """Draw scroll indicators for overlay popup"""
        # Position scroll bar on the right side of the popup, inside the bounds
        scrollbar_x = popup_bg_x + popup_width - 30  # 30px from right edge
        scrollbar_y = popup_bg_y + 60  # Start below title area
        scrollbar_height = popup_height - 120  # Leave space for title and spacing
        
        total_items = 10  # We know there are 10 overlay options
        self._draw_scrollbar(scrollbar_x, scrollbar_y, scrollbar_height,
                           total_items, items_per_page, scroll_offset)
    
    def draw_seed_scroll_indicators(self, popup_bg_x, popup_bg_y, popup_width, popup_height,
                                  scroll_offset, items_per_page):
        """Draw scroll indicators for seed selection popup"""
        # Position scroll bar on the right side of the popup, inside the bounds
        scrollbar_x = popup_bg_x + popup_width - 30  # 30px from right edge
        scrollbar_y = popup_bg_y + 60  # Start below title area
        scrollbar_height = popup_height - 120  # Leave space for title and spacing
        
        self._draw_scrollbar(scrollbar_x, scrollbar_y, scrollbar_height,
                           len(seeds_config), items_per_page, scroll_offset)
    
    def _draw_scrollbar(self, scrollbar_x, scrollbar_y, scrollbar_height, 
                       total_items, items_per_page, scroll_offset):
        """Draw a scrollbar with the given parameters"""
        # Scroll bar background
        scrollbar_bg = pyglet.shapes.Rectangle(
            scrollbar_x, scrollbar_y, 20, scrollbar_height,
            color=(40, 40, 40), batch=None
        )
        scrollbar_bg.draw()
        
        # Scroll position indicator
        if total_items <= items_per_page:
            return  # No scrolling needed
        
        visible_ratio = items_per_page / total_items
        scroll_ratio = scroll_offset / (total_items - items_per_page)
        
        indicator_height = max(20, scrollbar_height * visible_ratio)
        indicator_y = scrollbar_y + (scrollbar_height - indicator_height) * scroll_ratio
        
        scroll_indicator = pyglet.shapes.Rectangle(
            scrollbar_x + 2, indicator_y, 16, indicator_height,
            color=(100, 100, 100), batch=None
        )
        scroll_indicator.draw()

