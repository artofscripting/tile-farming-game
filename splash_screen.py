import pyglet

class SplashScreen(pyglet.window.Window):
    def __init__(self, next_callback, *args, **kwargs):
        super().__init__(caption="A Tile Farming Game", *args, **kwargs)
        # Set window icon
        try:
            icon = pyglet.image.load('forest.ico')
            self.set_icon(icon)
        except Exception:
            pass
        self.next_callback = next_callback
        self.splash_image = pyglet.image.load('img/title.png')
        scale = 0.5
        self.splash_sprite = pyglet.sprite.Sprite(self.splash_image, x=0, y=0)
        self.splash_sprite.scale = scale
        splash_width = int(self.splash_image.width * scale)
        splash_height = int(self.splash_image.height * scale)
        self.set_size(splash_width, splash_height)
        # Center window on screen
        screen = self.screen
        if screen:
            self.set_location(
                int((screen.width - splash_width) / 2),
                int((screen.height - splash_height) / 2)
            )
        # Button properties
        self.button_width = 200
        self.button_height = 60
        self.button_x = (splash_width - self.button_width) // 2
        self.button_y = 160
        self.button_label = pyglet.text.Label(
            'New Game',
            font_name='Arial',
            font_size=28,
            color=(255,255,255,255),
            x=self.button_x + self.button_width//2,
            y=self.button_y + self.button_height//2,
            anchor_x='center', anchor_y='center'
        )
        self.button_rect = pyglet.shapes.Rectangle(
            self.button_x, self.button_y,
            self.button_width, self.button_height,
            color=(50, 120, 50)
        )
        self.button_hover = False

    def on_draw(self):
        self.clear()
        self.splash_sprite.draw()
        self.button_rect.draw()
        self.button_label.draw()

    def on_key_press(self, symbol, modifiers):
        self.finish()

    def on_mouse_motion(self, x, y, dx, dy):
        self.button_hover = self.button_x <= x <= self.button_x + self.button_width and \
                            self.button_y <= y <= self.button_y + self.button_height
        self.button_rect.color = (80, 180, 80) if self.button_hover else (50, 120, 50)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.button_x <= x <= self.button_x + self.button_width and \
           self.button_y <= y <= self.button_y + self.button_height:
            self.finish()

    def finish(self):
        self.next_callback()
        self.close()
