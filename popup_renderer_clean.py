import pyglet
from constants import seeds_config

class PopupRenderer:
    def __init__(self, popup_core):
        self.core = popup_core

    def draw(self):
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
        self.draw_popup_tooltip()

    def draw_building_selection_popup(self):
        pass

    def draw_seed_type_selection_popup(self):
        pass

    def draw_seed_bin_selection_popup(self):
        pass

    def draw_fertilizer_selection_popup(self):
        pass

    def draw_tractor_upgrade_popup(self):
        pass

    def draw_overlay_selection_popup(self):
        pass

    def draw_seed_selection_popup(self):
        pass

    def draw_popup_tooltip(self):
        pass

