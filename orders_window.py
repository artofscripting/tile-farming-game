import pyglet
from constants import *


class OrdersPopup:
    """Popup to display crop orders from outside buyers"""
    def __init__(self, game_state, order_system, game_window=None):
        self.game_state = game_state
        self.order_system = order_system
        self.game_window = game_window
        self.incoming_scroll_offset = 0
        self.accepted_scroll_offset = 0
        self.max_visible_incoming = 5  # Show 5 incoming orders at a time
        self.max_visible_accepted = 5  # Show 5 accepted orders at a time
        self.is_open = False  # Track if popup is currently open

        # Colors
        self.bg_color = (0.1, 0.1, 0.1, 0.9)
        self.header_color = (0.2, 0.2, 0.2, 1.0)
        self.text_color = (1, 1, 1, 1)
        self.accent_color = (77, 153, 77, 255)  # Green for accepted
        self.warning_color = (153, 77, 77, 255)  # Red for expired

        # Popup dimensions (centered on game area)
        self.width = 760
        self.height = 420

        # Center on entire window
        if game_window:
            self.x = (game_window.width - self.width) // 2
            self.y = (game_window.height - self.height) // 2
        else:
            # Fallback to screen centering if no game window provided
            self.x = (800 - self.width) // 2
            self.y = (600 - self.height) // 2

    def show(self):
        """Show the orders popup"""
        self.is_open = True

    def hide(self):
        """Hide the orders popup"""
        self.is_open = False

    def toggle(self):
        """Toggle the popup visibility"""
        self.is_open = not self.is_open

    def draw(self):
        """Draw the orders popup on the main window"""
        if not self.is_open:
            return

        # Draw semi-transparent background overlay covering entire window
        if self.game_window:
            overlay = pyglet.shapes.Rectangle(0, 0, self.game_window.width, self.game_window.height, color=(0, 0, 0, 150))
        else:
            # Fallback if no game window reference
            overlay = pyglet.shapes.Rectangle(0, 0, 800, 600, color=(0, 0, 0, 150))
        overlay.draw()

        # Draw popup background
        bg_rect = pyglet.shapes.Rectangle(
            self.x, self.y, self.width, self.height,
            color=(40, 40, 40)
        )
        bg_rect.draw()

        # Header background
        header_rect = pyglet.shapes.Rectangle(
            self.x, self.y + self.height - 40, self.width, 40,
            color=(60, 60, 60)
        )
        header_rect.draw()

        # Draw close button
        close_btn = pyglet.shapes.Rectangle(
            self.x + self.width - 30, self.y + self.height - 30,
            20, 20, color=(200, 50, 50)
        )
        close_btn.draw()
        pyglet.text.Label(
            'X', font_size=12,
            x=self.x + self.width - 20, y=self.y + self.height - 20,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255)
        ).draw()

        # Draw title
        pyglet.text.Label(
            'Crop Orders', font_size=18,
            x=self.x + self.width // 2, y=self.y + self.height - 25,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255)
        ).draw()

        # Draw section headers
        pyglet.text.Label(
            'Incoming Orders', font_size=14,
            x=self.x + 20, y=self.y + self.height - 70,
            color=(255, 255, 0, 255)
        ).draw()

        pyglet.text.Label(
            'Accepted Orders', font_size=14,
            x=self.x + self.width // 2 + 20, y=self.y + self.height - 70,
            color=(0, 255, 0, 255)
        ).draw()

        # Draw scroll buttons
        # Incoming orders scroll buttons (right of incoming section)
        incoming_up_btn = pyglet.shapes.Rectangle(
            self.x + 325, self.y + self.height - 85, 20, 15, color=(100, 100, 100)
        )
        incoming_up_btn.draw()
        pyglet.text.Label(
            '↑', font_size=10,
            x=self.x + 335, y=self.y + self.height - 80,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255)
        ).draw()

        incoming_down_btn = pyglet.shapes.Rectangle(
            self.x + 325, self.y + 30, 20, 15, color=(100, 100, 100)
        )
        incoming_down_btn.draw()
        pyglet.text.Label(
            '↓', font_size=10,
            x=self.x + 335, y=self.y + 35,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255)
        ).draw()

        # Accepted orders scroll buttons (right of accepted section)
        accepted_up_btn = pyglet.shapes.Rectangle(
            self.x + self.width // 2 + 345, self.y + self.height - 85, 20, 15, color=(100, 100, 100)
        )
        accepted_up_btn.draw()
        pyglet.text.Label(
            '↑', font_size=10,
            x=self.x + self.width // 2 + 355, y=self.y + self.height - 80,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255)
        ).draw()

        accepted_down_btn = pyglet.shapes.Rectangle(
            self.x + self.width // 2 + 345, self.y + 30, 20, 15, color=(100, 100, 100)
        )
        accepted_down_btn.draw()
        pyglet.text.Label(
            '↓', font_size=10,
            x=self.x + self.width // 2 + 355, y=self.y + 35,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255)
        ).draw()

        # Draw orders content
        self.draw_orders_content()

    def draw_orders_content(self):
        """Draw the orders list with scrolling"""
        y_offset = self.y + self.height - 100

        # Draw incoming orders (left side)
        incoming_orders = self.order_system.get_incoming_orders()
        start_idx = self.incoming_scroll_offset
        end_idx = min(start_idx + self.max_visible_incoming, len(incoming_orders))

        for i in range(start_idx, end_idx):
            display_idx = i - start_idx
            order_y = y_offset - display_idx * 65  # Increased spacing to 65 pixels for more space
            self.draw_order(incoming_orders[i], self.x + 20, order_y, is_incoming=True)
            
            # Draw separator line between orders (not after the last one)
            if i < end_idx - 1:
                separator_y = order_y - 45  # Position line 9 pixels below the order (more padding)
                separator_rect = pyglet.shapes.Rectangle(
                    self.x + 20, separator_y - 1,  # Center the 2px line
                    self.width // 2 - 40, 2,  # Width: from x+20 to x+width//2-20, 2px height
                    color=(120, 120, 120)  # Slightly brighter gray
                )
                separator_rect.draw()

        # Draw accepted orders (right side)
        accepted_orders = self.order_system.get_accepted_orders()
        start_idx = self.accepted_scroll_offset
        end_idx = min(start_idx + self.max_visible_accepted, len(accepted_orders))

        for i in range(start_idx, end_idx):
            display_idx = i - start_idx
            order_y = y_offset - display_idx * 65  # Increased spacing to 65 pixels for more space
            self.draw_order(accepted_orders[i], self.x + self.width // 2 + 20, order_y, is_incoming=False)
            
            # Draw separator line between orders (not after the last one)
            if i < end_idx - 1:
                separator_y = order_y - 45  # Position line 9 pixels below the order (more padding)
                separator_rect = pyglet.shapes.Rectangle(
                    self.x + self.width // 2 + 20, separator_y - 1,  # Center the 2px line
                    self.width // 2 - 40, 2,  # Width: from x+width//2+20 to x+width-20, 2px height
                    color=(120, 120, 120)  # Slightly brighter gray
                )
                separator_rect.draw()
                separator_rect.draw()

    def draw_order(self, order, x, y, is_incoming=True):
        """Draw a single order"""

        # Order text
        crop_text = f"{order.crop_name}: {order.get_remaining_quantity()}/{order.quantity}"
        price_text = f"${order.premium_price:.2f}/unit"
        
        # Time info - show age and due date for both incoming and accepted orders
        current_day = self.game_window.market.current_day if self.game_window and hasattr(self.game_window, 'market') else 0
        age_days = int(order.get_age_days(current_day))
        age_text = f"Age: {age_days} days"
        due_day = order.created_day + order.duration_days
        due_text = f"Due: Day {due_day}"
        time_text = None  # No separate time text needed

        # Color based on status
        current_day = self.game_window.market.current_day if self.game_window and hasattr(self.game_window, 'market') else 0
        if order.is_expired(current_day):
            color = self.warning_color
        elif is_incoming:
            color = (255, 255, 0, 255)  # Yellow for incoming
        else:
            color = self.accent_color  # Green for accepted

        # Draw order info
        pyglet.text.Label(
            crop_text, font_size=10,
            x=x, y=y,
            color=color
        ).draw()

        pyglet.text.Label(
            price_text, font_size=10,
            x=x, y=y - 12,
            color=color
        ).draw()

        # Draw age on separate line for all orders
        if age_text:
            pyglet.text.Label(
                age_text, font_size=9,
                x=x, y=y - 24,
                color=color
            ).draw()

        # Draw due date on separate line for all orders
        if due_text:
            pyglet.text.Label(
                due_text, font_size=9,
                x=x, y=y - 36,
                color=color
            ).draw()

        # Draw accept/reject buttons for incoming orders
        if is_incoming:
            # Accept button (green)
            accept_btn = pyglet.shapes.Rectangle(
                x + 200, y - 5, 40, 20, color=(50, 150, 50)
            )
            accept_btn.draw()
            pyglet.text.Label(
                'Accept', font_size=8,
                x=x + 220, y=y + 5,
                anchor_x='center', anchor_y='center',
                color=(255, 255, 255, 255)
            ).draw()

            # Reject button (red)
            reject_btn = pyglet.shapes.Rectangle(
                x + 250, y - 5, 40, 20, color=(150, 50, 50)
            )
            reject_btn.draw()
            pyglet.text.Label(
                'Reject', font_size=8,
                x=x + 270, y=y + 5,
                anchor_x='center', anchor_y='center',
                color=(255, 255, 255, 255)
            ).draw()
        else:
            # Complete button for accepted orders (blue)
            complete_btn = pyglet.shapes.Rectangle(
                x + 200, y - 5, 50, 20, color=(50, 100, 200)
            )
            complete_btn.draw()
            pyglet.text.Label(
                'Complete', font_size=8,
                x=x + 225, y=y + 5,
                anchor_x='center', anchor_y='center',
                color=(255, 255, 255, 255)
            ).draw()

            # Cancel button for accepted orders (red)
            cancel_btn = pyglet.shapes.Rectangle(
                x + 260, y - 5, 45, 20, color=(150, 50, 50)
            )
            cancel_btn.draw()
            pyglet.text.Label(
                'Cancel', font_size=8,
                x=x + 282, y=y + 5,
                anchor_x='center', anchor_y='center',
                color=(255, 255, 255, 255)
            ).draw()

    def handle_mouse_press(self, x, y, button, modifiers):
        """Handle mouse clicks in the popup (called from main window)"""
        if not self.is_open:
            return False

        # Convert screen coordinates to popup coordinates
        popup_x = x - self.x
        popup_y = y - self.y

        # Check if click is within popup bounds
        if not (0 <= popup_x <= self.width and 0 <= popup_y <= self.height):
            return False  # Click outside popup

        # Check close button
        if (self.width - 30 <= popup_x <= self.width - 10 and
            self.height - 30 <= popup_y <= self.height - 10):
            self.hide()
            return True

        # Check scroll buttons
        # Incoming orders scroll buttons
        if (325 <= popup_x <= 345 and self.height - 85 <= popup_y <= self.height - 70):
            # Incoming up button
            if self.incoming_scroll_offset > 0:
                self.incoming_scroll_offset -= 1
            return True
        elif (325 <= popup_x <= 345 and 30 <= popup_y <= 45):
            # Incoming down button
            max_scroll = max(0, len(self.order_system.get_incoming_orders()) - self.max_visible_incoming)
            if self.incoming_scroll_offset < max_scroll:
                self.incoming_scroll_offset += 1
            return True

        # Accepted orders scroll buttons
        if (self.width // 2 + 345 <= popup_x <= self.width // 2 + 365 and self.height - 85 <= popup_y <= self.height - 70):
            # Accepted up button
            if self.accepted_scroll_offset > 0:
                self.accepted_scroll_offset -= 1
            return True
        elif (self.width // 2 + 345 <= popup_x <= self.width // 2 + 365 and 30 <= popup_y <= 45):
            # Accepted down button
            max_scroll = max(0, len(self.order_system.get_accepted_orders()) - self.max_visible_accepted)
            if self.accepted_scroll_offset < max_scroll:
                self.accepted_scroll_offset += 1
            return True

        # Check accept/reject buttons for incoming orders
        y_offset = self.height - 100
        incoming_orders = self.order_system.get_incoming_orders()
        start_idx = self.incoming_scroll_offset
        end_idx = min(start_idx + self.max_visible_incoming, len(incoming_orders))

        for i in range(start_idx, end_idx):
            display_idx = i - start_idx
            order_x = 20
            order_y = y_offset - display_idx * 65  # Updated spacing to match drawing

            # Accept button
            if (order_x + 200 <= popup_x <= order_x + 240 and
                order_y - 5 <= popup_y <= order_y + 15):
                self.order_system.accept_order(incoming_orders[i])
                return True

            # Reject button
            if (order_x + 250 <= popup_x <= order_x + 290 and
                order_y - 5 <= popup_y <= order_y + 15):
                self.order_system.reject_order(incoming_orders[i])
                return True

        # Check complete buttons for accepted orders
        accepted_orders = self.order_system.get_accepted_orders()
        start_idx = self.accepted_scroll_offset
        end_idx = min(start_idx + self.max_visible_accepted, len(accepted_orders))

        for i in range(start_idx, end_idx):
            display_idx = i - start_idx
            order_x = self.width // 2 + 20
            order_y = y_offset - display_idx * 65  # Updated spacing to match drawing

            # Complete button
            if (order_x + 200 <= popup_x <= order_x + 250 and
                order_y - 5 <= popup_y <= order_y + 15):
                remaining_quantity = accepted_orders[i].get_remaining_quantity()
                crop_name = accepted_orders[i].crop_name
                available_quantity = self.order_system.get_total_barn_storage(crop_name)

                if available_quantity < remaining_quantity:
                    return True

                success = self.order_system.complete_order(accepted_orders[i])
                if success:
                    # Force UI info window to update immediately after order completion
                    if hasattr(self.game_state, 'game_window') and hasattr(self.game_state.game_window, 'ui_info_window'):
                        try:
                            self.game_state.game_window.ui_info_window._update_info()
                        except Exception as e:
                            print(f"Warning: Could not update UI info window: {e}")
                return True

            # Cancel button
            if (order_x + 260 <= popup_x <= order_x + 305 and
                order_y - 5 <= popup_y <= order_y + 15):
                self.order_system.cancel_order(accepted_orders[i])
                return True

        return True  # Click was inside popup but not on any button

    def handle_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """Handle mouse wheel scrolling in the popup (called from main window)"""
        if not self.is_open:
            return False

        # Convert screen coordinates to popup coordinates
        popup_x = x - self.x
        popup_y = y - self.y

        # Check if mouse is within popup bounds
        if not (0 <= popup_x <= self.width and 0 <= popup_y <= self.height):
            return False  # Mouse outside popup

        # Determine which list the mouse is over
        if popup_x < self.width // 2:
            # Left side - incoming orders
            if scroll_y > 0:  # Scroll up
                if self.incoming_scroll_offset > 0:
                    self.incoming_scroll_offset -= 1
            elif scroll_y < 0:  # Scroll down
                max_scroll = max(0, len(self.order_system.get_incoming_orders()) - self.max_visible_incoming)
                if self.incoming_scroll_offset < max_scroll:
                    self.incoming_scroll_offset += 1
        else:
            # Right side - accepted orders
            if scroll_y > 0:  # Scroll up
                if self.accepted_scroll_offset > 0:
                    self.accepted_scroll_offset -= 1
            elif scroll_y < 0:  # Scroll down
                max_scroll = max(0, len(self.order_system.get_accepted_orders()) - self.max_visible_accepted)
                if self.accepted_scroll_offset < max_scroll:
                    self.accepted_scroll_offset += 1

        return True

