"""
Tile interaction handling for farming operations
"""
from pyglet.window import key
from constants import (
    MOUSE_MODE_NORMAL, MOUSE_MODE_TRACTOR, MOUSE_MODE_BUY_TILES, 
    MOUSE_MODE_PLANT_SEEDS, MOUSE_MODE_HARVEST, MOUSE_MODE_BUILD, 
    MOUSE_MODE_CULTIVATE, MOUSE_MODE_CULTIVATOR, game_config, seeds_config,
    TILE_BARN, TILE_SEED_BIN, TILE_TILLED, TILE_GROWING, TILE_READY_HARVEST,
    BUILDING_SEED_BIN
)
from tractor_job_queue import JobType


class TileInteractionHandler:
    """Handles interactions with farm tiles based on current mouse mode"""
    
    def __init__(self, game_window):
        self.game_window = game_window
    
    def get_seed_price(self, seed_name):
        """Get the price of a specific seed type from seeds config"""
        for seed in seeds_config:
            if seed['name'] == seed_name:
                return seed['cost']
        return 10  # Default fallback price
    
    def handle_tile_interaction(self, tile, grid_x, grid_y, modifiers=0, is_double_click=False):
        """Handle interactions with farm tiles based on current mode"""
        if self.game_window.mouse_mode == MOUSE_MODE_NORMAL:
            self._handle_normal_mode_interaction(tile, modifiers, is_double_click)
        elif self.game_window.mouse_mode == MOUSE_MODE_TRACTOR:
            self._handle_tractor_mode_interaction(tile, grid_x, grid_y)
        elif self.game_window.mouse_mode == MOUSE_MODE_BUY_TILES:
            self._handle_buy_tiles_mode_interaction(tile, grid_x, grid_y, modifiers)
        elif self.game_window.mouse_mode == MOUSE_MODE_PLANT_SEEDS:
            self._handle_plant_seeds_mode_interaction(tile, grid_x, grid_y)
        elif self.game_window.mouse_mode == MOUSE_MODE_HARVEST:
            self._handle_harvest_mode_interaction(tile, grid_x, grid_y)
        elif self.game_window.mouse_mode == MOUSE_MODE_CULTIVATE:
            self._handle_cultivate_mode_interaction(tile, grid_x, grid_y)
        elif self.game_window.mouse_mode == MOUSE_MODE_CULTIVATOR:
            self._handle_cultivator_mode_interaction(tile, grid_x, grid_y)
        elif self.game_window.mouse_mode == MOUSE_MODE_BUILD:
            self._handle_build_mode_interaction(tile, modifiers)
    
    def _handle_normal_mode_interaction(self, tile, modifiers, is_double_click=False):
        """Handle tile interactions in normal mode"""
        # Import here to avoid circular import
        from input_building_handler import BuildingInteractionHandler
        building_handler = BuildingInteractionHandler(self.game_window)
        
        if tile.state == TILE_BARN:
            building_handler.interact_with_building(tile, modifiers)
        elif tile.state == TILE_SEED_BIN:
            if is_double_click:
                # Show seed bin management popup on double-click
                self.game_window.popup_system.show_seed_bin_management_popup(tile)
            else:
                building_handler.handle_seed_bin_left_click(tile, modifiers)
    
    def _handle_tractor_mode_interaction(self, tile, grid_x, grid_y):
        """Handle tile interactions in tractor mode"""
        success = False
        available_tractor = self.game_window.get_available_tractor()
        if available_tractor:
            # Use multi-row tilling based on tractor upgrade mode
            num_rows = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
            success = available_tractor.start_tilling_multi_row(grid_y, self.game_window.width, self.game_window, grid_x, num_rows)
        else:
            # No tractor available, queue the job
            num_rows = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
            success = self.game_window.tractor_job_queue.add_job(
                JobType.TILLING, grid_x, grid_y, num_rows=num_rows
            )
        if success:
            if available_tractor:
                print("Tractor started tilling!")
            else:
                print("Tilling job queued - will start when tractor becomes available!")
    
    def _handle_buy_tiles_mode_interaction(self, tile, grid_x, grid_y, modifiers):
        """Handle tile interactions in buy tiles mode"""
        if tile.state == 0:  # TILE_UNOWNED
            is_shift_pressed = modifiers & key.MOD_SHIFT
            is_ctrl_pressed = modifiers & key.MOD_CTRL
            
            if is_shift_pressed:
                # Buy all 8 surrounding tiles if they are unowned and player has enough money
                from input_purchase_handler import PurchaseHandler
                purchase_handler = PurchaseHandler(self.game_window)
                purchase_handler.buy_surrounding_tiles(tile, grid_x, grid_y)
            elif is_ctrl_pressed:
                # Buy entire row if they are unowned and player has enough money
                from input_purchase_handler import PurchaseHandler
                purchase_handler = PurchaseHandler(self.game_window)
                purchase_handler.buy_entire_row(tile, grid_x, grid_y)
            else:
                # Buy single tile
                if self.game_window.game_state.can_afford(game_config['tile_purchase_price']):
                    if self.game_window.game_state.spend_money(game_config['tile_purchase_price'], 
                                                             'tile_purchase', 
                                                             f"Purchased tile at ({grid_x},{grid_y})", 
                                                             {'x': grid_x, 'y': grid_y}):
                        tile.set_state(1)  # TILE_OWNED
                        print(f"Purchased tile for ${game_config['tile_purchase_price']}")
    
    def _handle_plant_seeds_mode_interaction(self, tile, grid_x, grid_y):
        """Handle tile interactions in plant seeds mode"""
        if tile.state == 2:  # TILE_TILLED
            selected_seed = self.game_window.game_state.selected_seed
            if selected_seed:
                # Check if we have seeds in seed bins
                has_seeds = False
                for bin_tile in self.game_window.farm_tiles:
                    if (bin_tile.state == TILE_SEED_BIN and 
                        bin_tile.stored_crop_type == selected_seed and 
                        bin_tile.stored_amount > 0):
                        has_seeds = True
                        break
                
                if has_seeds:
                    success = False
                    available_tractor = self.game_window.get_available_tractor()
                    if available_tractor:
                        # Use multi-row planting based on tractor upgrade mode
                        num_rows = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
                        success = available_tractor.start_planting_multi_row(grid_y, self.game_window.width, self.game_window, grid_x, selected_seed, num_rows)
                    else:
                        # No tractor available, queue the job
                        num_rows = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
                        success = self.game_window.tractor_job_queue.add_job(
                            JobType.PLANTING, grid_x, grid_y, seed_type=selected_seed, num_rows=num_rows
                        )
                    if success:
                        if available_tractor:
                            print(f"Tractor started planting {selected_seed} seeds from seed bins!")
                        else:
                            print(f"Planting {selected_seed} job queued - will start when tractor becomes available!")
                else:
                    print(f"No {selected_seed} seeds available in seed bins!")
            else:
                print("No seed type selected!")
    
    def _handle_harvest_mode_interaction(self, tile, grid_x, grid_y):
        """Handle tile interactions in harvest mode"""
        if tile.state == 5:  # TILE_READY_HARVEST
            success = False
            available_tractor = self.game_window.get_available_tractor()
            if available_tractor:
                # Use multi-row harvesting based on tractor upgrade mode
                num_rows = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
                success = available_tractor.start_harvesting_multi_row(grid_y, self.game_window.width, self.game_window, grid_x, num_rows)
            else:
                # No tractor available, queue the job
                num_rows = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
                success = self.game_window.tractor_job_queue.add_job(
                    JobType.HARVESTING, grid_x, grid_y, num_rows=num_rows
                )
            if success:
                if available_tractor:
                    print("Tractor started harvesting crops!")
                else:
                    print("Harvesting job queued - will start when tractor becomes available!")
    
    def _handle_cultivate_mode_interaction(self, tile, grid_x, grid_y):
        """Handle tile interactions in cultivate mode"""
        cultivatable_states = [TILE_TILLED, TILE_GROWING, TILE_READY_HARVEST]
        
        if tile.state in cultivatable_states:
            selected_fertilizer = self.game_window.game_state.selected_fertilizer
            if selected_fertilizer:
                success = False
                available_tractor = self.game_window.get_available_tractor()
                if available_tractor:
                    # Use multi-row cultivating based on tractor upgrade mode
                    num_rows = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
                    success = available_tractor.start_cultivating_multi_row(
                        grid_y, self.game_window.width, self.game_window, grid_x, selected_fertilizer, num_rows
                    )
                else:
                    # No tractor available, queue the job
                    num_rows = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
                    success = self.game_window.tractor_job_queue.add_job(
                        JobType.FERTILIZING, grid_x, grid_y, fertilizer_data=selected_fertilizer, num_rows=num_rows
                    )
                if success:
                    if available_tractor:
                        print(f"Tractor started cultivating with {selected_fertilizer['name']} fertilizer!")
                    else:
                        print(f"Cultivating with {selected_fertilizer['name']} job queued - will start when tractor becomes available!")
            else:
                print("No fertilizer selected!")
        else:
            print("Can only cultivate tilled, growing, or harvest-ready tiles!")
    
    def _handle_cultivator_mode_interaction(self, tile, grid_x, grid_y):
        """Handle tile interactions in cultivator mode"""
        success = False
        available_tractor = self.game_window.get_available_tractor()
        if available_tractor:
            # Use multi-row cultivator based on tractor upgrade mode
            num_rows = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
            success = available_tractor.start_cultivator_multi_row(grid_y, self.game_window.width, self.game_window, grid_x, num_rows)
        else:
            # No tractor available, queue the job
            num_rows = getattr(self.game_window.game_state, 'tractor_row_mode', 1)
            success = self.game_window.tractor_job_queue.add_job(
                JobType.CULTIVATOR, grid_x, grid_y, num_rows=num_rows
            )
        if success:
            if available_tractor:
                print("Tractor started removing weeds!")
            else:
                print("Weed removal job queued - will start when tractor becomes available!")
        else:
            print("Cannot start cultivator tractor on this tile!")
    
    def _handle_build_mode_interaction(self, tile, modifiers):
        """Handle tile interactions in build mode"""
        if tile.state == 1:  # TILE_OWNED
            # Build the selected structure
            if tile.build_structure(self.game_window.selected_building):
                from constants import game_config
                if self.game_window.selected_building == "barn":
                    building_cost = game_config['barn_place_cost']
                else:
                    building_cost = game_config['seed_bin_place_cost']
                if self.game_window.game_state.spend_money(building_cost, 
                                                         'building_construction', 
                                                         f"Built {self.game_window.selected_building}", 
                                                         {'building_type': self.game_window.selected_building, 'cost': building_cost}):
                    # Set up seed bin with selected seed type
                    if (self.game_window.selected_building == BUILDING_SEED_BIN and 
                        self.game_window.popup_system.selected_seed_type):
                        tile.store_crop(self.game_window.popup_system.selected_seed_type, 1)  # Start with 1 seed
                        print(f"Built {self.game_window.selected_building} for ${building_cost} with {self.game_window.popup_system.selected_seed_type} seeds")
                    else:
                        print(f"Built {self.game_window.selected_building} for ${building_cost}")
                    self.game_window.mouse_mode = MOUSE_MODE_NORMAL
                    self.game_window.reset_all_buttons()
                    self.game_window.set_mouse_cursor(None)
                else:
                    # Undo building if can't afford
                    tile.set_state(1)  # TILE_OWNED
                    tile.building_type = None
                    print(f"Cannot afford {self.game_window.selected_building} (${building_cost})")
            else:
                print("Cannot build on this tile!")
        elif tile.state in [TILE_BARN, TILE_SEED_BIN]:
            # Interact with existing building
            from input_building_handler import BuildingInteractionHandler
            building_handler = BuildingInteractionHandler(self.game_window)
            building_handler.interact_with_building(tile, modifiers)

