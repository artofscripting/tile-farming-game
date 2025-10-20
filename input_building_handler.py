"""
Building interaction handling for barns and seed bins
"""
from pyglet.window import key
from constants import TILE_BARN, TILE_SEED_BIN, seeds_config


class BuildingInteractionHandler:
    """Handles interactions with buildings like barns and seed bins"""
    
    def __init__(self, game_window):
        self.game_window = game_window
    
    def get_seed_price(self, seed_name):
        """Get the price of a specific seed type from seeds config"""
        for seed in seeds_config:
            if seed['name'] == seed_name:
                return seed['cost']
        return 10  # Default fallback price
    
    def interact_with_building(self, tile, modifiers=0):
        """Handle interactions with buildings"""
        if tile.state == TILE_SEED_BIN:
            # Buy seeds from seed bin
            if tile.stored_amount <= 0:
                print("Seed bin is empty!")
                return
                
            is_shift_pressed = modifiers & key.MOD_SHIFT
            quantity = min(10 if is_shift_pressed else 1, tile.stored_amount)  # Can't buy more than available
            
            # Get seed price for the specific seed type in the bin
            seed_type = tile.stored_crop_type
            seed_price = self.get_seed_price(seed_type) if seed_type else 10
            total_cost = seed_price * quantity
            
            if self.game_window.game_state.can_afford(total_cost):
                if self.game_window.game_state.spend_money(total_cost, 
                                                         'seed_purchase', 
                                                         f"Bulk seed purchase: {quantity}x {seed_type}", 
                                                         {'seed_type': seed_type, 'quantity': quantity}):
                    # Use the seed type from the bin
                    seed_type = tile.stored_crop_type
                    if seed_type and seed_type in self.game_window.game_state.seed_inventory:
                        # Remove seeds from bin and add to player inventory
                        removed_type, removed_amount = tile.remove_crop(quantity)
                        if removed_type:
                            self.game_window.game_state.seed_inventory[seed_type] += removed_amount
                            print(f"Bought {removed_amount} {seed_type} seeds for ${total_cost}")
                            print(f"Seed bin now has {tile.stored_amount} {seed_type} seeds remaining")
                        else:
                            # Refund if couldn't remove from bin
                            self.game_window.game_state.earn_money(total_cost)
                            print("Error: Could not remove seeds from bin!")
                    else:
                        # Refund if seed type not found
                        self.game_window.game_state.earn_money(total_cost)
                        print(f"Error: {seed_type} not found in inventory!")
                else:
                    print(f"Cannot afford {quantity} seeds (${total_cost})")
            else:
                print(f"Cannot afford {quantity} seeds (${total_cost})")
                
        elif tile.state == TILE_BARN:
            # Check if shift is pressed for upgrading
            is_shift_pressed = modifiers & key.MOD_SHIFT
            
            if is_shift_pressed:
                # Upgrade barn capacity
                tile.upgrade_barn(self.game_window.game_state)
            else:
                # Show barn info on regular left-click
                if tile.stored_amount > 0:
                    print(f"Barn contains {tile.stored_amount} {tile.stored_crop_type}")
                    print(f"Barn capacity: {tile.stored_amount}/{tile.building_capacity}")
                else:
                    print(f"Barn is empty - capacity: {tile.stored_amount}/{tile.building_capacity}")
    
    def buy_seeds_from_bin(self, tile, modifiers=0):
        """Handle right-click purchases of seeds for seed bins"""
        if tile.state != TILE_SEED_BIN:
            return
            
        # Determine quantity based on shift key
        is_shift_pressed = modifiers & key.MOD_SHIFT
        quantity = 10 if is_shift_pressed else 1
        
        # Check if we have a previous seed type stored (even if bin is empty)
        previous_seed_type = getattr(tile, 'previous_seed_type', None)
        current_seed_type = tile.stored_crop_type
        
        # Determine the seed type to use
        seed_type_to_use = current_seed_type or previous_seed_type
        
        # If we have a seed type (current or previous), use it directly
        if seed_type_to_use:
            seed_price = self.get_seed_price(seed_type_to_use)
            total_cost = seed_price * quantity
            
            if not self.game_window.game_state.can_afford(total_cost):
                print(f"Cannot afford {quantity} {seed_type_to_use} seeds (${total_cost})")
                return
                
            # Check space available
            space_available = tile.building_capacity - tile.stored_amount
            quantity_to_add = min(quantity, space_available)
            
            if quantity_to_add <= 0:
                print(f"Seed bin is full! (Capacity: {tile.building_capacity})")
                return
            
            # Calculate actual cost for what we can add
            actual_cost = seed_price * quantity_to_add
            
            if self.game_window.game_state.spend_money(actual_cost, 
                                                     'seed_purchase', 
                                                     f"Purchased {quantity_to_add}x {seed_type_to_use}", 
                                                     {'seed_type': seed_type_to_use, 'quantity': quantity_to_add}):
                tile.store_crop(seed_type_to_use, quantity_to_add)
                print(f"Added {quantity_to_add} {seed_type_to_use} seeds to bin for ${actual_cost}")
                print(f"Seed bin now has {tile.stored_amount} {seed_type_to_use} seeds")
                
                if quantity_to_add < quantity:
                    print(f"Could only add {quantity_to_add} seeds due to capacity limit")
        else:
            # No seed type available (completely new bin), show popup to select seed type
            self.game_window.popup_system.pending_seed_purchase = {
                'tile': tile,
                'quantity': quantity,
                'total_cost': 0  # Will be calculated based on selected seed type
            }
            self.game_window.popup_system.show_seed_type_selection_popup()
    
    def handle_seed_bin_left_click(self, tile, modifiers=0):
        """Handle left-click on seed bin for upgrades"""
        if tile.state != TILE_SEED_BIN:
            return
        
        # Check if shift is pressed for upgrading
        is_shift_pressed = modifiers & key.MOD_SHIFT
        
        if is_shift_pressed:
            # Upgrade seed bin capacity
            tile.upgrade_seed_bin(self.game_window.game_state)
        else:
            # Show seed bin info on regular left-click
            print(f"Seed bin capacity: {tile.stored_amount}/{tile.building_capacity}")
            if tile.stored_crop_type:
                print(f"Contains: {tile.stored_crop_type}")
            else:
                print("Empty seed bin")
    
    def handle_barn_right_click(self, tile, modifiers=0):
        """Handle right-click on barn for selling contents"""
        if tile.state != TILE_BARN:
            return
            
        # Check if barn has contents to sell
        if tile.stored_amount <= 0:
            print("Barn is empty - nothing to sell!")
            return
            
        # Check if shift is pressed for selling all contents
        is_shift_pressed = modifiers & key.MOD_SHIFT
        
        if is_shift_pressed:
            # Sell all contents
            crop_type = tile.stored_crop_type
            amount_to_sell = tile.stored_amount
            
            # Get current market price
            market_price = self.game_window.market.get_price(crop_type)
            total_value = market_price * amount_to_sell
            
            # Remove all crops from barn and give money to player
            removed_type, removed_amount = tile.remove_crop(amount_to_sell)
            if removed_type and removed_amount > 0:
                self.game_window.game_state.earn_money(total_value)
                print(f"Sold {removed_amount} {removed_type} from barn for ${total_value} (${market_price}/unit)")
                print(f"Barn is now empty")
            else:
                print("Error: Could not sell barn contents!")
        else:
            # Just show barn contents (no selling without shift)
            print(f"Barn contains {tile.stored_amount} {tile.stored_crop_type}")
            print("Hold Shift + Right-click to sell all contents")

