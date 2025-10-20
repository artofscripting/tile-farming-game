import pyglet


class Button:
    def __init__(self, x, y, width, height, text, batch):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.batch = batch
        self.pressed = False
        self._visible = True  # Add visible property
        
        # Create button background (simple rectangle)
        self.background = pyglet.shapes.Rectangle(
            x, y, width, height, color=(0, 50, 0), batch=batch
        )
        self.border = pyglet.shapes.Rectangle(
            x, y, width, height, color=(200, 200, 200), batch=batch
        )
        self.border.opacity = 0
        
        # Create text label
        self.label = pyglet.text.Label(
            text, x=x + width//2, y=y + height//2,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255), batch=batch
        )
        
        self._update_visibility()
    
    @property
    def visible(self):
        return self._visible
    
    @visible.setter
    def visible(self, value):
        self._visible = value
        self._update_visibility()
        
    def _update_visibility(self):
        """Update the visibility of all button elements"""
        opacity = 255 if self._visible else 0
        self.background.opacity = opacity
        self.border.opacity = 0 if not self._visible else (255 if self.pressed else 0)
        self.label.color = (255, 255, 255, opacity) if self._visible else (255, 255, 255, 0)
        
    def contains_point(self, x, y):
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def set_pressed(self, pressed):
        self.pressed = pressed
        if self._visible:  # Only update appearance if visible
            if pressed:
                self.background.color = (0, 75, 0)  # Darker green when pressed
                self.border.opacity = 255
            else:
                self.background.color = (0, 50, 0)  # Dark green when not pressed
                self.border.opacity = 0
    
    def draw(self):
        """Draw the button (for manual drawing when not using batch)"""
        if self._visible:
            self.background.draw()
            self.border.draw()
            self.label.draw()

