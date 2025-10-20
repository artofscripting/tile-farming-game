"""
Background rendering for popups
"""
import pyglet


class PopupBackgroundRenderer:
    """Handles popup background rendering"""
    
    def __init__(self, game_window):
        self.game_window = game_window
    
    def draw_standard_background(self, title, width=300, height=350):
        """Draw standard popup background with semi-transparent overlay"""
        # Semi-transparent overlay
        overlay = pyglet.shapes.Rectangle(
            0, 0, self.game_window.width, self.game_window.height,
            color=(0, 0, 0), batch=None
        )
        overlay.opacity = 128
        overlay.draw()
        
        # Popup background
        popup_bg_x = self.game_window.width // 2 - width // 2
        popup_bg_y = self.game_window.height // 2 - height // 2
        
        popup_bg = pyglet.shapes.Rectangle(
            popup_bg_x, popup_bg_y, width, height,
            color=(0, 40, 0), batch=None
        )
        popup_bg.draw()
        
        # Title text
        title_y_offset = 40 if "Select Seed Type for Seed Bin" in title else 30
        title_label = pyglet.text.Label(
            title,
            x=self.game_window.width // 2,
            y=popup_bg_y + height - title_y_offset,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255),
            font_size=16
        )
        title_label.draw()
        
        return popup_bg_x, popup_bg_y, width, height
    
    def draw_building_background(self, title):
        """Draw building selection popup background"""
        return self.draw_standard_background(title)
    
    def draw_seed_type_background(self, title):
        """Draw seed type selection popup background"""
        # Wider and taller for seed type selection
        width = 420
        height = 460
        return self.draw_standard_background(title, width, height)
    
    def draw_seed_bin_background(self, title):
        """Draw seed bin selection popup background"""
        return self.draw_standard_background(title)
    
    def draw_fertilizer_background(self, title):
        """Draw fertilizer popup background with custom size"""
        # Semi-transparent overlay
        overlay = pyglet.shapes.Rectangle(
            0, 0, self.game_window.width, self.game_window.height,
            color=(0, 0, 0), batch=None
        )
        overlay.opacity = 128
        overlay.draw()
        
        # Fertilizer popup background - larger size
        width = 500
        height = 400
        popup_bg_x = self.game_window.width // 2 - width // 2
        popup_bg_y = self.game_window.height // 2 - height // 2
        
        popup_bg = pyglet.shapes.Rectangle(
            popup_bg_x, popup_bg_y, width, height,
            color=(0, 40, 0), batch=None
        )
        popup_bg.draw()
        
        # Title text
        title_label = pyglet.text.Label(
            title,
            x=self.game_window.width // 2,
            y=popup_bg_y + height - 30,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255),
            font_size=16
        )
        title_label.draw()
        
        return popup_bg_x, popup_bg_y, width, height
    
    def draw_tractor_upgrade_background(self, title):
        """Draw tractor upgrade popup background"""
        # Semi-transparent overlay
        overlay = pyglet.shapes.Rectangle(
            0, 0, self.game_window.width, self.game_window.height,
            color=(0, 0, 0), batch=None
        )
        overlay.opacity = 128
        overlay.draw()
        
        # Tractor upgrade popup background - wider to fit longer button text
        width = 350
        height = 350
        popup_bg_x = self.game_window.width // 2 - width // 2
        popup_bg_y = self.game_window.height // 2 - height // 2
        
        popup_bg = pyglet.shapes.Rectangle(
            popup_bg_x, popup_bg_y, width, height,
            color=(0, 40, 0), batch=None
        )
        popup_bg.draw()
        
        # Title text
        title_label = pyglet.text.Label(
            title,
            x=self.game_window.width // 2,
            y=popup_bg_y + height - 30,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255),
            font_size=16
        )
        title_label.draw()
        
        return popup_bg_x, popup_bg_y, width, height
    
    def draw_overlay_background(self, title):
        """Draw overlay selection popup background"""
        # Semi-transparent overlay
        overlay = pyglet.shapes.Rectangle(
            0, 0, self.game_window.width, self.game_window.height,
            color=(0, 0, 0), batch=None
        )
        overlay.opacity = 128
        overlay.draw()
        
        # Larger popup background for overlay selection
        width = 400  # Increased to fit content
        height = 450  # Increased to fit content
        popup_bg_x = self.game_window.width // 2 - width // 2
        popup_bg_y = self.game_window.height // 2 - height // 2
        
        popup_bg = pyglet.shapes.Rectangle(
            popup_bg_x, popup_bg_y, width, height,
            color=(0, 40, 0), batch=None
        )
        popup_bg.draw()
        
        # Title text
        title_label = pyglet.text.Label(
            title,
            x=self.game_window.width // 2,
            y=popup_bg_y + height - 30,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255),
            font_size=16
        )
        title_label.draw()
        
        return popup_bg_x, popup_bg_y, width, height
    
    def draw_seed_selection_background(self, title):
        """Draw seed selection popup background"""
        return self.draw_overlay_background(title)
    
    def draw_seed_bin_management_background(self, title):
        """Draw seed bin management popup background"""
        return self.draw_standard_background(title, width=400, height=300)

