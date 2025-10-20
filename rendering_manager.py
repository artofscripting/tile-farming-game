"""
Rendering Manager - Handles all drawing and rendering functionality
"""
import pyglet
from constants import farm_batch, icon_batch, tractor_batch, ui_batch


class RenderingManager:
    def __init__(self, game_window):
        self.game_window = game_window
    
    def draw_background(self):
        """Draw the game background"""
        # Draw main farm area background (bright green)
        main_background = pyglet.shapes.Rectangle(
            0, 0, self.game_window.width - 245, self.game_window.height,
            color=(51, 153, 51)  # Bright green for farm area
        )
        main_background.draw()
        
        # Draw UI background area (very dark green rectangle)
        ui_background = pyglet.shapes.Rectangle(
            self.game_window.width - 245, 0, 245, self.game_window.height, 
            color=(0, 25, 0)  # Very dark green for UI area
        )
        ui_background.draw()
        
        # Draw separator line
        separator_line = pyglet.shapes.Line(
            self.game_window.width - 245, 0, self.game_window.width - 245, self.game_window.height,
            batch=None, color=(255, 255, 255)  # White line
        )
        separator_line.draw()
    
    def draw_game_batches(self):
        """Draw all game batches with error handling"""
        # Draw farm batch (background layer)
        farm_batch.draw()
        
        # Draw icon batch (foreground layer - icons on top of buildings)
        icon_batch.draw()
        
        # Draw hover tile highlight
        self.game_window.managers.hover_system.draw_hover_tile_highlight()
        
        # Draw queue visualization
        self.draw_queue_indicators()
        
        # Draw tractor batch with error handling
        try:
            tractor_batch.draw()
        except Exception as e:
            # If tractor batch fails to draw, recreate it
            print(f"Tractor batch drawing error: {e}")
            self.game_window.managers.tractor_manager.rebuild_tractor_batch()
        
        # Draw UI batch with error handling
        try:
            ui_batch.draw()
        except Exception as e:
            # If UI batch fails to draw, try to recover by clearing and rebuilding it
            print(f"UI batch drawing error: {e}")
            try:
                # Clear the problematic batch and create a new one
                import constants
                new_ui_batch = pyglet.graphics.Batch()
                # Replace the corrupted batch in constants
                constants.ui_batch = new_ui_batch
                print("UI batch cleared and recreated due to OpenGL error")
            except Exception as recovery_error:
                print(f"Failed to recover UI batch: {recovery_error}")
                # Continue without the UI batch
                pass
    
    def draw_ui_elements(self):
        """Draw UI elements"""
        # Draw UI information
        self.game_window.ui_manager.draw_ui_info()
        self.game_window.ui_manager.draw_mode_indicators()
        
        # Draw row mode indicator in bottom right of right panel
        self.game_window.ui_manager.draw_row_mode_indicator()
        
        # Draw tractor job queue status
        self.game_window.ui_manager.draw_queue_status()
        
        # Draw tooltip if available (but not over popups)
        if self.game_window.tooltip_system.should_draw(self.game_window.popup_system.is_showing_popup()):
            self.game_window.tooltip_system.draw()
        
        # Draw popups
        self.game_window.popup_system.draw()
        
        # Draw orders window (removed - now handled by separate window)
    
    def draw_queue_indicators(self):
        """Draw purple tint and tractor icons on tiles with queued jobs"""
        if hasattr(self.game_window, 'tractor_job_queue'):
            queued_positions = self.game_window.tractor_job_queue.get_queued_positions()
            
            for grid_x, grid_y in queued_positions:
                # Draw light purple tint overlay on the tile
                from constants import grid_size
                purple_tint = pyglet.shapes.Rectangle(
                    grid_x, grid_y, grid_size, grid_size,  # Use grid_size for tile size
                    color=(128, 0, 128)  # Purple color
                )
                purple_tint.opacity = 80  # Semi-transparent (0-255 scale)
                purple_tint.draw()
                
                # Draw a simple yellow circle as tractor indicator (more reliable than huge image)
                tractor_indicator = pyglet.shapes.Circle(
                    x=grid_x + grid_size // 2,  # Center in tile
                    y=grid_y + grid_size // 2,
                    radius=grid_size // 4,
                    color=(255, 255, 0)  # Yellow color for visibility
                )
                tractor_indicator.draw()
                
                # Also try to draw the tractor image if it works
                try:
                    from constants import tractor_image
                    if tractor_image and tractor_image.width > 0:
                        # Create a much smaller scale for the huge 4000x4000 image
                        target_size = 12  # Target 12x12 pixels (smaller)
                        scale_factor = target_size / max(tractor_image.width, tractor_image.height)
                        
                        tractor_sprite = pyglet.sprite.Sprite(
                            tractor_image,
                            x=grid_x + (grid_size - target_size) // 2,  # Center in tile
                            y=grid_y + (grid_size - target_size) // 2
                        )
                        tractor_sprite.scale = scale_factor
                        tractor_sprite.draw()
                except Exception as e:
                    pass  # Fall back to just the yellow circle
    
    def render_frame(self):
        """Render a complete frame"""
        # Clear with default background
        self.game_window.clear()
        
        # Draw background
        self.draw_background()
        
        # Draw game batches
        self.draw_game_batches()
        
        # Draw overlays
        self.game_window.overlay_manager.draw()
        
        # Draw UI elements
        self.draw_ui_elements()
        
        # Draw notification
        self.draw_notification()
        
        # Draw orders popup (on top of everything else)
        if hasattr(self.game_window, 'orders_window') and self.game_window.orders_window:
            self.game_window.orders_window.draw()
    
    def draw_notification(self):
        """Draw notification message in bottom left of game area"""
        if self.game_window.notification_message and self.game_window.notification_timer > 0:
            # Position in bottom left of game area (not UI panel)
            x = 20
            y = 20
            
            # Draw semi-transparent background
            bg_width = 200
            bg_height = 40
            notification_bg = pyglet.shapes.Rectangle(
                x - 10, y - 5, bg_width, bg_height,
                color=(0, 0, 0), batch=None
            )
            notification_bg.opacity = 180
            notification_bg.draw()
            
            # Draw notification text
            notification_label = pyglet.text.Label(
                self.game_window.notification_message,
                x=x, y=y + 10,
                anchor_x='left',
                anchor_y='center',
                color=(255, 255, 255, 255),
                font_size=14
            )
            notification_label.draw()

