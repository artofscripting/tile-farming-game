import pyglet

class GameEvents:
    def __init__(self, game_window):
        self.game_window = game_window
        # Add event handlers
        game_window.push_handlers(self)

    def on_key_press(self, symbol, modifiers):
        """Handle keyboard input"""
        # Track Shift key state
        if symbol == pyglet.window.key.LSHIFT or symbol == pyglet.window.key.RSHIFT:
            self.game_window.managers.hover_system.set_shift_pressed(True)
        # Track Control key state
        elif symbol == pyglet.window.key.LCTRL or symbol == pyglet.window.key.RCTRL:
            self.game_window.managers.hover_system.set_ctrl_pressed(True)
        
        self.game_window.input_handler.handle_key_press(symbol, modifiers)
    
    def on_key_release(self, symbol, modifiers):
        """Handle key release events"""
        # Track Shift key state
        if symbol == pyglet.window.key.LSHIFT or symbol == pyglet.window.key.RSHIFT:
            self.game_window.managers.hover_system.set_shift_pressed(False)
        # Track Control key state
        elif symbol == pyglet.window.key.LCTRL or symbol == pyglet.window.key.RCTRL:
            self.game_window.managers.hover_system.set_ctrl_pressed(False)

    def on_mouse_motion(self, x, y, dx, dy):
        """Handle mouse movement"""
        self.game_window.tooltip_system.update_mouse_position(x, y)
        self.game_window.popup_system.update_mouse_position(x, y)
        
        # Update hover tile position through hover system
        self.game_window.managers.hover_system.update_hover_position(x, y)
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse button presses"""
        # Check orders popup first (blocks other input when open)
        if hasattr(self.game_window, 'orders_window') and self.game_window.orders_window and self.game_window.orders_window.is_open:
            if self.game_window.orders_window.handle_mouse_press(x, y, button, modifiers):
                return  # Popup handled the input

        self.game_window.input_handler.handle_mouse_press(x, y, button, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """Handle mouse wheel scrolling"""
        # Check orders popup first (blocks other scrolling when open)
        if hasattr(self.game_window, 'orders_window') and self.game_window.orders_window and self.game_window.orders_window.is_open:
            if self.game_window.orders_window.handle_mouse_scroll(x, y, scroll_x, scroll_y):
                return  # Popup handled the scrolling

        # If fertilizer popup is showing, handle scrolling
        if self.game_window.popup_system.show_fertilizer_popup:
            if scroll_y > 0:  # Scroll up
                if self.game_window.popup_system.core.fertilizer_scroll_offset > 0:
                    self.game_window.popup_system.core.fertilizer_scroll_offset -= 1
                    self.game_window.popup_system.fertilizer._update_fertilizer_buttons()
            elif scroll_y < 0:  # Scroll down
                max_items = len(self.game_window.popup_system.core.fertilizer_config)
                items_per_page = self.game_window.popup_system.core.fertilizer_items_per_page
                max_offset = max(0, max_items - items_per_page)
                if self.game_window.popup_system.core.fertilizer_scroll_offset < max_offset:
                    self.game_window.popup_system.core.fertilizer_scroll_offset += 1
                    self.game_window.popup_system.fertilizer._update_fertilizer_buttons()

        # If seed type popup is showing, handle scrolling
        elif self.game_window.popup_system.show_seed_type_popup:
            if scroll_y > 0:  # Scroll up
                if self.game_window.popup_system.core.seed_type_scroll_offset > 0:
                    self.game_window.popup_system.core.seed_type_scroll_offset -= 1
                    self.game_window.popup_system.seeds._update_seed_type_buttons()
            elif scroll_y < 0:  # Scroll down
                from constants import seeds_config
                max_items = len(seeds_config)
                items_per_page = self.game_window.popup_system.core.seed_type_items_per_page
                max_offset = max(0, max_items - items_per_page)
                if self.game_window.popup_system.core.seed_type_scroll_offset < max_offset:
                    self.game_window.popup_system.core.seed_type_scroll_offset += 1
                    self.game_window.popup_system.seeds._update_seed_type_buttons()

        # If overlay popup is showing, handle scrolling
        elif self.game_window.popup_system.show_overlay_popup:
            if scroll_y > 0:  # Scroll up
                if self.game_window.popup_system.core.overlay_scroll_offset > 0:
                    self.game_window.popup_system.core.overlay_scroll_offset -= 1
                    self.game_window.popup_system.overlays._update_overlay_buttons()
            elif scroll_y < 0:  # Scroll down
                max_items = len(self.game_window.popup_system.overlays.overlay_options)
                items_per_page = self.game_window.popup_system.core.overlay_items_per_page
                max_offset = max(0, max_items - items_per_page)
                if self.game_window.popup_system.core.overlay_scroll_offset < max_offset:
                    self.game_window.popup_system.core.overlay_scroll_offset += 1
                    self.game_window.popup_system.overlays._update_overlay_buttons()

    def on_mouse_leave(self, x, y):
        """Handle mouse leaving the window"""
        self.game_window.tooltip_system.hide_tooltip()

    def on_mouse_enter(self, x, y):
        """Handle mouse entering the window"""
        pass

    def on_close(self):
        """Handle window close event"""
        # Save game on exit
        self.game_window.save_game()
        pyglet.app.exit()

    def update(self, dt):
        """Update game state"""
        # Update all tractors
        for tractor in self.game_window.tractors:
            tractor.update(dt, self.game_window)

        # Process tractor job queue when tractors become available
        self.game_window.tractor_job_queue.process_queue()

        # Check if tractors have finished their tasks and show messages
        for tractor in self.game_window.tractors:
            if hasattr(tractor, 'show_completion_message') and tractor.show_completion_message:
                if tractor.task_type == "tilling":
                    print("Tractor finished tilling the row!")
                elif tractor.task_type == "planting":
                    print(f"Tractor finished planting {tractor.seed_type} seeds!")
                elif tractor.task_type == "harvesting":
                    print("Tractor finished harvesting crops!")
                elif tractor.task_type == "cultivating":
                    print(f"Tractor finished cultivating with {tractor.fertilizer_type['name']} fertilizer!")

                tractor.show_completion_message = False

        # Update crop growth
        for tile in self.game_window.farm_tiles:
            tile.update_growth()

        # Update market prices and check for new day
        old_day = self.game_window.market.current_day
        self.game_window.market.update(dt)

        # If a new day has started, grow weeds on all farm tiles
        if self.game_window.market.current_day != old_day:
            self.grow_weeds_daily()

        # Update order system (generate new orders periodically)
        self.game_window.game_state.order_system.update()

        # Update tooltip content every tick for dynamic data
        self.game_window.tooltip_system.update_tooltip_tick()

        # Update notification timer
        if self.game_window.notification_timer > 0:
            self.game_window.notification_timer -= dt
            if self.game_window.notification_timer <= 0:
                self.game_window.notification_message = None

        # Update row mode button visibility and text
        self.game_window.ui_manager.update_row_mode_button()

        # Auto-save every 2 minutes
        self.game_window.auto_save_timer += dt
        if self.game_window.auto_save_timer >= self.game_window.auto_save_interval:
            self.game_window.auto_save_game()
            self.game_window.auto_save_timer = 0.0

    def grow_weeds_daily(self):
        """Grow weeds on all farm tiles at the start of each new day"""
        total_tiles_affected = 0
        total_weed_growth = 0

        for tile in self.game_window.farm_tiles:
            weed_growth = tile.grow_weeds()
            if weed_growth > 0:
                total_tiles_affected += 1
                total_weed_growth += weed_growth

        if total_tiles_affected > 0:
            avg_growth = total_weed_growth / total_tiles_affected
            print(f"🌿 Daily weed growth: {total_tiles_affected} tiles affected, average +{avg_growth:.1f} weeds per tile")
