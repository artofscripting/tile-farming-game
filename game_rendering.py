class GameRendering:
    def __init__(self, game_window):
        self.game_window = game_window
        # Add rendering setup here
        game_window.push_handlers(self)

    def on_draw(self):
        """Render the game"""
        self.game_window.managers.rendering_manager.render_frame()
