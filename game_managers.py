from farm_manager import FarmManager
from tractor_manager import TractorManager
from hover_system import HoverSystem
from rendering_manager import RenderingManager
from overlay_manager import OverlayManager
from tractor_job_queue import TractorJobQueue

class GameManagers:
    def __init__(self, game_window):
        self.game_state = game_window.game_state
        self.market = game_window.market
        self.farm_manager = FarmManager(game_window)
        self.tractor_manager = TractorManager(game_window)
        self.hover_system = HoverSystem(game_window)
        self.rendering_manager = RenderingManager(game_window)
        self.overlay_manager = OverlayManager(game_window)
        self.tractor_job_queue = TractorJobQueue(game_window)
