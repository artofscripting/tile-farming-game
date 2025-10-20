import pyglet
from pyglet import shapes
from constants import fertilizer_config


class FertilizerInfoWindow(pyglet.window.Window):
    def __init__(self, game_window=None, *args, **kwargs):
        super().__init__(400, 300, 'Fertilizer Information', resizable=False, *args, **kwargs)

        self.game_window = game_window

        # Colors
        self.bg_color = (40, 40, 40)  # Dark gray background
        self.text_color = (255, 255, 255)  # White text
        self.header_color = (100, 200, 255)  # Light blue for headers
        self.nutrient_color = (150, 255, 150)  # Light green for nutrient values

        # Create fertilizer information labels
        self.create_fertilizer_labels()

        # Create title label (after window is resized)
        self.title_label = pyglet.text.Label(
            'Fertilizer Information',
            font_name='Arial',
            font_size=20,
            x=self.width // 2,
            y=self.height - 15,
            anchor_x='center',
            anchor_y='top',
            color=self.header_color + (255,)
        )

        # Create subtitle
        self.subtitle_label = pyglet.text.Label(
            'Nutrient Effects per Application',
            font_name='Arial',
            font_size=12,
            x=self.width // 2,
            y=self.height - 45,
            anchor_x='center',
            anchor_y='top',
            color=self.text_color + (255,)
        )

    def calculate_column_widths(self, columns):
        """Calculate appropriate widths for each column based on content"""
        from constants import fertilizer_config
        
        col_widths = []
        padding = 10  # Extra padding for each column
        
        for i, col_name in enumerate(columns):
            max_width = 0
            
            # Measure header width
            header_label = pyglet.text.Label(col_name, font_name='Arial', font_size=12)
            max_width = max(max_width, header_label.content_width)
            
            # Measure data content width
            if col_name == 'Fertilizer':
                # Check all fertilizer names
                for fertilizer in fertilizer_config:
                    name_label = pyglet.text.Label(fertilizer['name'], font_name='Arial', font_size=10)
                    max_width = max(max_width, name_label.content_width)
            elif col_name == 'Cost':
                # Check all cost values
                for fertilizer in fertilizer_config:
                    cost_text = f"${fertilizer['cost']}"
                    cost_label = pyglet.text.Label(cost_text, font_name='Arial', font_size=10)
                    max_width = max(max_width, cost_label.content_width)
            else:
                # Nutrient columns - check values
                nutrient_key = None
                if col_name == 'Nit':
                    nutrient_key = 'nitrogen'
                elif col_name == 'Pho':
                    nutrient_key = 'phosphorus'
                elif col_name == 'Pot':
                    nutrient_key = 'potassium'
                elif col_name == 'Cal':
                    nutrient_key = 'calcium'
                elif col_name == 'Mag':
                    nutrient_key = 'magnesium'
                elif col_name == 'Sul':
                    nutrient_key = 'sulfur'
                elif col_name == 'Wat':
                    nutrient_key = 'water'
                
                if nutrient_key:
                    for fertilizer in fertilizer_config:
                        value = fertilizer.get(nutrient_key, 0)
                        value_text = str(value) if value > 0 else '-'
                        value_label = pyglet.text.Label(value_text, font_name='Arial', font_size=10)
                        max_width = max(max_width, value_label.content_width)
            
            col_widths.append(max_width + padding)
        
        return col_widths
    
    def calculate_column_positions(self, col_widths):
        """Calculate x positions for column centers based on widths"""
        positions = []
        current_x = 20  # Left margin
        
        for width in col_widths:
            center_x = current_x + width // 2
            positions.append(center_x)
            current_x += width
        
        return positions
    
    def add_label(self, label):
        """Add a label to be drawn"""
        if not hasattr(self, '_labels'):
            self._labels = []
        self._labels.append(label)

    def add_shape(self, shape):
        """Add a shape to be drawn"""
        if not hasattr(self, '_shapes'):
            self._shapes = []
        self._shapes.append(shape)

    def create_fertilizer_labels(self):
        """Create labels displaying fertilizer information in table format"""
        from constants import fertilizer_config
        
        row_height = 25  # Height of each row
        header_margin = 80  # Space for title and subtitle
        bottom_margin = 20  # Bottom margin
        
        # Calculate required height
        num_rows = len(fertilizer_config) + 1  # +1 for header row
        required_height = header_margin + (num_rows * row_height) + bottom_margin
        
        # Resize window height if needed
        if required_height > self.height:
            self.set_size(self.width, int(required_height))
        
        y_start = self.height - header_margin
        nutrient_names = ['Nitrogen', 'Phosphorus', 'Potassium', 'Calcium', 'Magnesium', 'Sulfur', 'Water']
        columns = ['Fertilizer'] + [n[:3] for n in nutrient_names] + ['Cost']  # Abbreviated names for space
        
        # Calculate column widths based on content
        col_widths = self.calculate_column_widths(columns)
        col_positions = self.calculate_column_positions(col_widths)
        
        # Adjust window width to fit content
        total_width = sum(col_widths) + 40  # 40 for margins
        if total_width > self.width:
            # Resize window if needed
            self.set_size(int(total_width), self.height)
            # Recalculate positions with new width
            col_positions = self.calculate_column_positions(col_widths)
        
        # Create header row
        for i, col_name in enumerate(columns):
            header_label = pyglet.text.Label(
                col_name,
                font_name='Arial',
                font_size=12,
                x=col_positions[i],
                y=y_start,
                anchor_x='center',
                anchor_y='center',
                color=self.header_color + (255,)
            )
            self.add_label(header_label)
        
        # Create data rows
        for i, fertilizer in enumerate(fertilizer_config):
            y_pos = y_start - ((i + 1) * row_height)
            
            # Fertilizer name column
            name_label = pyglet.text.Label(
                fertilizer['name'],
                font_name='Arial',
                font_size=10,
                x=col_positions[0],
                y=y_pos,
                anchor_x='center',
                anchor_y='center',
                color=self.text_color + (255,)
            )
            self.add_label(name_label)
            
            # Nutrient value columns
            for j, nutrient in enumerate(nutrient_names):
                key = nutrient.lower()
                value = fertilizer.get(key, 0)
                value_text = str(value) if value > 0 else '-'
                
                nutrient_label = pyglet.text.Label(
                    value_text,
                    font_name='Arial',
                    font_size=10,
                    x=col_positions[j + 1],
                    y=y_pos,
                    anchor_x='center',
                    anchor_y='center',
                    color=self.nutrient_color + (255,) if value > 0 else self.text_color + (128,)  # Dimmed for zero values
                )
                self.add_label(nutrient_label)
            
            # Cost column
            cost_label = pyglet.text.Label(
                f"${fertilizer['cost']}",
                font_name='Arial',
                font_size=10,
                x=col_positions[-1],
                y=y_pos,
                anchor_x='center',
                anchor_y='center',
                color=(255, 215, 0, 255)  # Gold color for cost
            )
            self.add_label(cost_label)
            
            # Separator line between rows (except after last row)
            if i < len(fertilizer_config) - 1:
                separator = shapes.Line(
                    10, y_pos - 10, self.width - 10, y_pos - 10,
                    color=(100, 100, 100)
                )
                self.add_shape(separator)

    def on_draw(self):
        """Draw the window"""
        self.clear()
        pyglet.gl.glClearColor(*[c/255 for c in self.bg_color], 1)

        # Draw background
        batch = pyglet.graphics.Batch()
        background = shapes.Rectangle(0, 0, self.width, self.height,
                                   color=self.bg_color, batch=batch)
        batch.draw()

        # Draw title and subtitle
        self.title_label.draw()
        self.subtitle_label.draw()

        # Draw labels
        if hasattr(self, '_labels'):
            for label in self._labels:
                label.draw()

        # Draw shapes
        if hasattr(self, '_shapes'):
            for shape in self._shapes:
                shape.draw()

    def on_key_press(self, symbol, modifiers):
        """Handle key presses"""
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
            if self.game_window:
                self.game_window.fertilizer_info_window = None
                print("Fertilizer info window closed")

    def on_close(self):
        """Handle window close"""
        if self.game_window:
            self.game_window.fertilizer_info_window = None
        super().on_close()

