import pyglet
import os
import json
from constants import grid_size

class WindowSetup:
    @staticmethod
    def create_window(game_config, map_width, map_height, ui_border_right, *args, **kwargs):
        window_width = map_width * grid_size + ui_border_right
        window_height = map_height * grid_size
        window = pyglet.window.Window(width=window_width, height=window_height, caption="A Tile Farming Game", *args, **kwargs)
        try:
            icon = pyglet.image.load('forest.ico')
            window.set_icon(icon)
        except Exception:
            pass
        screen = window.screen
        if screen:
            window.set_location(
                int((screen.width - window_width) / 2),
                int((screen.height - window_height) / 2)
            )
        return window
