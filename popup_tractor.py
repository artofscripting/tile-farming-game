from constants import tractor_config

class PopupTractor:
    """Handles tractor upgrade popup"""
    
    def __init__(self, popup_core):
        self.core = popup_core
    
    def show_tractor_upgrade_popup(self):
        """Show popup to select tractor row operation mode"""
        self.core.show_building_popup = False
        self.core.show_seed_type_popup = False
        self.core.show_seed_bin_popup = False
        self.core.show_fertilizer_popup = False
        self.core.show_tractor_upgrade = True
        self.core.popup_buttons = []
        
        # Create popup buttons for tractor row selection
        popup_x = self.core.game_window.width // 2 - 125
        popup_y = self.core.game_window.height // 2
        
        # Check current tractor mode and purchase status
        current_mode = getattr(self.core.game_window.game_state, 'tractor_row_mode', 1)
        is_3_row_purchased = getattr(self.core.game_window.game_state, 'tractor_3_row_purchased', False)
        is_speed_purchased = getattr(self.core.game_window.game_state, 'tractor_speed_purchased', False)
        
        # 3-row mode button - show purchase option if not bought, otherwise mode selection
        if is_3_row_purchased:
            self.core.popup_buttons.append({
                'text': f'3 Row Mode {"(Current)" if current_mode == 3 else ""}',
                'x': popup_x, 'y': popup_y + 60,
                'width': 250, 'height': 40,
                'action': 'set_tractor_3_row'
            })
        else:
            # Show purchase option
            can_afford = self.core.game_window.game_state.can_afford(500)
            button_text = f'Buy 3 Row Mode - $500'
            if not can_afford:
                button_text += ' (Cannot Afford)'
            
            self.core.popup_buttons.append({
                'text': button_text,
                'x': popup_x, 'y': popup_y + 60,
                'width': 250, 'height': 40,
                'action': 'buy_tractor_3_row',
                'disabled': not can_afford
            })
        
        # Speed upgrade button
        if is_speed_purchased:
            self.core.popup_buttons.append({
                'text': 'Speed Boost (Active)',
                'x': popup_x, 'y': popup_y + 10,
                'width': 250, 'height': 40,
                'action': 'speed_info'
            })
        else:
            # Show purchase option
            can_afford_speed = self.core.game_window.game_state.can_afford(500)
            button_text = f'Buy Speed Boost - $500'
            if not can_afford_speed:
                button_text += ' (Cannot Afford)'
            
            self.core.popup_buttons.append({
                'text': button_text,
                'x': popup_x, 'y': popup_y + 10,
                'width': 250, 'height': 40,
                'action': 'buy_tractor_speed',
                'disabled': not can_afford_speed
            })
        
        # Buy Additional Tractor button
        current_tractor_count = len(self.core.game_window.managers.tractor_manager.tractors)
        prestige_cost = 30 + (current_tractor_count * 20)
        current_prestige = getattr(self.core.game_window.game_state, 'prestige', 0)
        can_afford_tractor = current_prestige >= prestige_cost
        tractor_button_text = f'Add Tractor {prestige_cost} Prestige'
        
        self.core.popup_buttons.append({
            'text': tractor_button_text,
            'x': popup_x, 'y': popup_y - 40,
            'width': 250, 'height': 40,
            'action': 'buy_additional_tractor',
            'disabled': not can_afford_tractor
        })
        
        self.core.popup_buttons.append({
            'text': 'Cancel',
            'x': popup_x, 'y': popup_y - 90,
            'width': 250, 'height': 40,
            'action': 'cancel'
        })
    
    def handle_tractor_action(self, action):
        """Handle tractor-related actions"""
        if action == 'set_tractor_3_row':
            self.core.game_window.game_state.tractor_row_mode = 3
            print("Tractor set to 3-row mode")
            self.core.close_popups()
            return True
            
        elif action == 'buy_tractor_3_row':
            # Check if button is disabled
            for button in self.core.popup_buttons:
                if button['action'] == action and button.get('disabled', False):
                    print("Cannot afford 3-row upgrade ($500)")
                    return True
            
            # Purchase the 3-row upgrade
            if self.core.game_window.game_state.spend_money(500):
                self.core.game_window.game_state.tractor_3_row_purchased = True
                self.core.game_window.game_state.tractor_row_mode = 3
                print("Purchased 3-row tractor upgrade for $500!")
                print("Tractor set to 3-row mode")
                # Update row mode button visibility now that upgrade is purchased
                self.core.game_window.ui_manager.update_row_mode_button()
                self.core.close_popups()
            else:
                print("Cannot afford 3-row upgrade ($500)")
            return True
            
        elif action == 'buy_tractor_speed':
            # Check if button is disabled
            for button in self.core.popup_buttons:
                if button['action'] == action and button.get('disabled', False):
                    print("Cannot afford speed upgrade ($500)")
                    return True
            
            # Purchase the speed upgrade
            if self.core.game_window.game_state.spend_money(500):
                self.core.game_window.game_state.tractor_speed_purchased = True
                # Update all existing tractors to use the new speed
                self._update_tractor_speeds()
                print("Purchased tractor speed boost for $500!")
                print("All tractors now move 100% faster!")
                self.core.close_popups()
            else:
                print("Cannot afford speed upgrade ($500)")
            return True
            
        elif action == 'speed_info':
            print("Speed boost is already active - tractors move 100% faster!")
            return True
            
        elif action == 'buy_additional_tractor':
            # Check if button is disabled
            for button in self.core.popup_buttons:
                if button['action'] == action and button.get('disabled', False):
                    current_tractor_count = len(self.core.game_window.managers.tractor_manager.tractors)
                    prestige_cost = 30 + (current_tractor_count * 20)
                    current_prestige = getattr(self.core.game_window.game_state, 'prestige', 0)
                    print(f"Cannot afford additional tractor ({prestige_cost} prestige needed, have {current_prestige})")
                    return True
            
            # Purchase additional tractor using the existing method
            self.core.game_window.purchase_tractor()
            self.core.close_popups()
            return True
            
        return False

    def _update_tractor_speeds(self):
        """Update speed for all existing tractors"""
        base_speed = 50
        upgraded_speed = int(base_speed * 2.0)  # 200% of base speed (100% faster)
        
        # Update all tractors in the tractor manager
        tractor_manager = self.core.game_window.managers.tractor_manager
        for tractor in tractor_manager.tractors:
            tractor.core.speed = upgraded_speed
            tractor.speed = upgraded_speed  # Update the exposed attribute too

