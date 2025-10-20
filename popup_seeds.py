from constants import (
    seeds_config, BUILDING_SEED_BIN, MOUSE_MODE_BUILD, MOUSE_MODE_PLANT_SEEDS,
    TILE_SEED_BIN
)
import pyglet


class PopupSeeds:
    """Handles seed type and seed bin selection popups"""
    
    def __init__(self, popup_core):
        self.core = popup_core
    
    def show_seed_type_selection_popup(self):
        """Show popup to select seed type for seed bin"""
        self.core.show_building_popup = False
        self.core.show_seed_type_popup = True
        self.core.popup_buttons = []
        self.core.seed_type_scroll_offset = 0  # Reset scroll
        
        self._update_seed_type_buttons()
    
    def _update_seed_type_buttons(self):
        """Update seed type popup buttons based on current scroll offset"""
        self.core.popup_buttons = []
        
        # Calculate popup background dimensions
        popup_width = 420  # Increased width to fit longer title
        popup_height = 460  # Increased height by 60px to accommodate more content
        popup_bg_x = self.core.game_window.width // 2 - popup_width // 2
        popup_bg_y = self.core.game_window.height // 2 - popup_height // 2
        
        # Position buttons relative to popup background
        popup_x = popup_bg_x + 60  # Center buttons with margin
        popup_y = popup_bg_y + popup_height - 110  # Start further below title for better spacing
        
        # Calculate visible range
        start_idx = self.core.seed_type_scroll_offset
        end_idx = min(start_idx + self.core.seed_type_items_per_page, len(seeds_config))
        
        # Create buttons for visible seed types
        for i, seed_idx in enumerate(range(start_idx, end_idx)):
            seed = seeds_config[seed_idx]
            
            self.core.popup_buttons.append({
                'text': f'{seed["name"]} Seeds',
                'x': popup_x, 'y': popup_y - i * 50,
                'width': 300, 'height': 45,  # Increased button width to match popup
                'action': f'select_seed_{seed["name"]}'
            })
        
        # Cancel button at bottom
        lowest_button_y = popup_y - (self.core.seed_type_items_per_page - 1) * 50
        cancel_y = lowest_button_y - 60
        self.core.popup_buttons.append({
            'text': 'Cancel',
            'x': popup_x, 'y': cancel_y,
            'width': 200, 'height': 45,
            'action': 'cancel'
        })
    
    def show_seed_bin_selection_popup(self):
        """Show popup to select seed bin for planting"""
        self.core.show_building_popup = False
        self.core.show_seed_type_popup = False
        self.core.show_seed_bin_popup = True
        self.core.show_fertilizer_popup = False
        self.core.popup_buttons = []
        
        # Find all seed bins with seeds
        available_seed_bins = []
        seed_type_totals = {}  # Track total seeds by type
        
        for tile in self.core.game_window.farm_tiles:
            if (tile.state == TILE_SEED_BIN and tile.stored_amount > 0 and 
                tile.stored_crop_type):
                seed_type = tile.stored_crop_type
                if seed_type not in seed_type_totals:
                    seed_type_totals[seed_type] = 0
                    available_seed_bins.append(tile)
                seed_type_totals[seed_type] += tile.stored_amount
        
        if not available_seed_bins:
            # No seed bins available
            popup_x = self.core.game_window.width // 2 - 100
            popup_y = self.core.game_window.height // 2
            self.core.popup_buttons.append({
                'text': 'No Seed Bins Available',
                'x': popup_x, 'y': popup_y + 20,
                'width': 200, 'height': 40,
                'action': 'none'
            })
            self.core.popup_buttons.append({
                'text': 'Cancel',
                'x': popup_x, 'y': popup_y - 30,
                'width': 200, 'height': 40,
                'action': 'cancel'
            })
        else:
            # Create popup buttons for seed bin selection
            popup_x = self.core.game_window.width // 2 - 125
            popup_y = self.core.game_window.height // 2 + 50
            
            for i, seed_type in enumerate(seed_type_totals.keys()):
                total_seeds = seed_type_totals[seed_type]
                self.core.popup_buttons.append({
                    'text': f'{seed_type} Seeds ({total_seeds} available)',
                    'x': popup_x, 'y': popup_y - i * 45,
                    'width': 250, 'height': 40,
                    'action': f'select_bin_{seed_type}'
                })
            
            self.core.popup_buttons.append({
                'text': 'Cancel',
                'x': popup_x, 'y': popup_y - len(seed_type_totals) * 45,
                'width': 250, 'height': 40,
                'action': 'cancel'
            })
    
    def show_seed_bin_management_popup(self, tile):
        """Show popup to manage seed bin (buy seeds/upgrade building)"""
        self.core.show_building_popup = False
        self.core.show_seed_type_popup = False
        self.core.show_seed_bin_popup = False
        self.core.show_fertilizer_popup = False
        self.core.show_tractor_upgrade = False
        self.core.show_overlay_popup = False
        self.core.show_seed_popup = False
        self.core.show_seed_bin_management = True
        self.core.popup_buttons = []
        self.core.managed_seed_bin_tile = tile
        
        # Calculate popup position
        popup_width = 400
        popup_height = 300
        popup_bg_x = self.core.game_window.width // 2 - popup_width // 2
        popup_bg_y = self.core.game_window.height // 2 - popup_height // 2
        
        # Position buttons relative to popup background
        popup_x = popup_bg_x + 50
        popup_y = popup_bg_y + popup_height - 80
        
        # Add buttons for seed bin management
        self.core.popup_buttons.append({
            'text': 'Buy Seeds',
            'x': popup_x, 'y': popup_y,
            'width': 300, 'height': 50,
            'action': 'manage_buy_seeds'
        })
        
        self.core.popup_buttons.append({
            'text': 'Upgrade Building',
            'x': popup_x, 'y': popup_y - 70,
            'width': 300, 'height': 50,
            'action': 'manage_upgrade_building'
        })
        
        # Cancel button
        self.core.popup_buttons.append({
            'text': 'Cancel',
            'x': popup_x, 'y': popup_y - 140,
            'width': 300, 'height': 50,
            'action': 'cancel'
        })
    
    def _get_upgrade_cost(self, tile):
        """Get the upgrade cost for a seed bin"""
        from constants import game_config
        return game_config['seed_bin_upgrade_cost']
    
    def show_seed_bin_management_popup(self, tile):
        """Show popup to manage seed bin (buy seeds/upgrade building)"""
        self.core.show_building_popup = False
        self.core.show_seed_type_popup = False
        self.core.show_seed_bin_popup = False
        self.core.show_fertilizer_popup = False
        self.core.show_seed_bin_management = True
        self.core.managed_seed_bin_tile = tile
        self.core.popup_buttons = []
        
        # Calculate popup dimensions and position
        popup_width = 400
        popup_height = 300
        popup_bg_x = self.core.game_window.width // 2 - popup_width // 2
        popup_bg_y = self.core.game_window.height // 2 - popup_height // 2
        
        # Position buttons relative to popup background
        button_x = popup_bg_x + 50
        button_y = popup_bg_y + popup_height - 100
        
        # Buy seeds button
        self.core.popup_buttons.append({
            'text': 'Buy Seeds',
            'x': button_x, 'y': button_y,
            'width': 300, 'height': 45,
            'action': 'manage_buy_seeds'
        })
        
        # Upgrade building button
        upgrade_cost = self._get_upgrade_cost(tile)
        self.core.popup_buttons.append({
            'text': f'Upgrade Building (${upgrade_cost})',
            'x': button_x, 'y': button_y - 60,
            'width': 300, 'height': 45,
            'action': 'manage_upgrade_building'
        })
        
        # Cancel button
        self.core.popup_buttons.append({
            'text': 'Cancel',
            'x': button_x, 'y': button_y - 150,
            'width': 300, 'height': 45,
            'action': 'cancel'
        })
    
    def _get_upgrade_cost(self, tile):
        """Get the upgrade cost for a seed bin"""
        # Base upgrade cost, could be made more sophisticated
        return 1000
    
    def handle_seed_action(self, action):
        """Handle seed-related actions"""
        if action.startswith('select_seed_'):
            seed_name = action.replace('select_seed_', '')
            
            # Check if this is for a pending seed purchase (right-click)
            if self.core.pending_seed_purchase:
                tile = self.core.pending_seed_purchase['tile']
                quantity = self.core.pending_seed_purchase['quantity']
                
                # Add seeds to the bin
                space_available = tile.building_capacity - tile.stored_amount
                quantity_to_add = min(quantity, space_available)
                
                if quantity_to_add > 0:
                    # Calculate actual cost for what we can add using correct seed price
                    actual_cost = self.core.get_seed_price(seed_name) * quantity_to_add
                    
                    if self.core.game_window.game_state.spend_money(actual_cost):
                        tile.store_crop(seed_name, quantity_to_add)
                        print(f"Added {quantity_to_add} {seed_name} seeds to bin for ${actual_cost}")
                        print(f"Seed bin now has {tile.stored_amount} {seed_name} seeds")
                        
                        if quantity_to_add < quantity:
                            print(f"Could only add {quantity_to_add} seeds due to capacity limit")
                    else:
                        print(f"Cannot afford {quantity_to_add} seeds (${actual_cost})")
                else:
                    print(f"Seed bin is full! (Capacity: {tile.building_capacity})")
                
                self.core.pending_seed_purchase = None
                self.core.close_popups()
            else:
                # Normal building mode
                self.core.game_window.selected_building = BUILDING_SEED_BIN
                self.core.selected_seed_type = seed_name
                self.core.close_popups()
                self.core.game_window.ui_manager.set_mode(MOUSE_MODE_BUILD, self.core.game_window.build_button)
            return True
            
        elif action.startswith('select_bin_'):
            seed_type = action.replace('select_bin_', '')
            self.core.selected_seed_bin = seed_type
            self.core.game_window.game_state.selected_seed = seed_type
            self.core.close_popups()
            self.core.game_window.ui_manager.set_mode(MOUSE_MODE_PLANT_SEEDS, self.core.game_window.plant_seeds_button)
            print(f"Selected {seed_type} seeds for planting from seed bins")
            return True
            
        elif action == 'manage_buy_seeds':
            # Buy seeds using the seed type already in the bin
            tile = self.core.managed_seed_bin_tile
            quantity = 10  # Default to buying 10 seeds
            
            # Get the seed type from the bin
            current_seed_type = tile.stored_crop_type
            if not current_seed_type:
                # If bin is empty, show seed type selection popup
                self.core.close_popups()
                self.core.pending_seed_purchase = {
                    'tile': tile,
                    'quantity': quantity,
                    'total_cost': 0
                }
                self.show_seed_type_selection_popup()
                return True
            
            # Calculate cost and check affordability
            seed_price = self.core.get_seed_price(current_seed_type)
            space_available = tile.building_capacity - tile.stored_amount
            quantity_to_add = min(quantity, space_available)
            
            if quantity_to_add <= 0:
                print(f"Seed bin is full! (Capacity: {tile.building_capacity})")
                self.core.close_popups()
                return True
            
            actual_cost = seed_price * quantity_to_add
            
            if not self.core.game_window.game_state.can_afford(actual_cost):
                print(f"Cannot afford {quantity_to_add} {current_seed_type} seeds (${actual_cost})")
                self.core.close_popups()
                return True
            
            # Purchase the seeds
            if self.core.game_window.game_state.spend_money(actual_cost):
                tile.store_crop(current_seed_type, quantity_to_add)
                print(f"Added {quantity_to_add} {current_seed_type} seeds to bin for ${actual_cost}")
                print(f"Seed bin now has {tile.stored_amount} {current_seed_type} seeds")
                
                if quantity_to_add < quantity:
                    print(f"Could only add {quantity_to_add} seeds due to capacity limit")
            else:
                print(f"Failed to purchase seeds")
            
            self.core.close_popups()
            return True
            
        elif action == 'manage_upgrade_building':
            # Upgrade the seed bin
            tile = self.core.managed_seed_bin_tile
            upgrade_cost = self._get_upgrade_cost(tile)
            
            if self.core.game_window.game_state.can_afford(upgrade_cost):
                if self.core.game_window.game_state.spend_money(upgrade_cost, 
                                                             'building_upgrade', 
                                                             f"Upgraded seed bin capacity", 
                                                             {'building_type': 'seed_bin', 'cost': upgrade_cost}):
                    tile.upgrade_seed_bin(self.core.game_window.game_state)
                    print(f"Upgraded seed bin for ${upgrade_cost}")
                else:
                    print(f"Cannot afford seed bin upgrade (${upgrade_cost})")
            else:
                print(f"Cannot afford seed bin upgrade (${upgrade_cost})")
            
            self.core.close_popups()
            return True
            
        return False

