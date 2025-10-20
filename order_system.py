import random
import time
from constants import seeds_config
from finance import TransactionType


class Order:
    """Represents a single crop order from an outside buyer"""
    def __init__(self, crop_name, quantity, premium_price, duration_days, creation_day=0):
        self.crop_name = crop_name
        self.quantity = quantity
        self.premium_price = premium_price  # Price per unit
        self.duration_days = duration_days
        self.created_day = creation_day  # Game day when order was created
        self.accepted = False
        self.fulfilled_quantity = 0

    def get_remaining_quantity(self):
        """Get remaining quantity to fulfill"""
        return self.quantity - self.fulfilled_quantity

    def is_expired(self, current_day):
        """Check if order has expired"""
        elapsed_days = current_day - self.created_day
        return elapsed_days >= self.duration_days

    def get_age_days(self, current_day):
        """Get the age of the order in days"""
        return current_day - self.created_day

    def fulfill(self, amount):
        """Fulfill part or all of the order"""
        if amount > self.get_remaining_quantity():
            amount = self.get_remaining_quantity()
        self.fulfilled_quantity += amount
        return amount

    def is_complete(self):
        """Check if order is fully fulfilled"""
        return self.fulfilled_quantity >= self.quantity


class OrderSystem:
    """Manages crop orders from outside buyers"""
    def __init__(self, game_state):
        self.game_state = game_state
        self.game_window = None  # Will be set later
        self.incoming_orders = []  # Orders that haven't been accepted yet
        self.accepted_orders = []  # Orders that have been accepted
        self.last_order_generation = time.time()
        self.last_day_processed = -1  # Track the last day we processed orders
        self.order_generation_interval = 7 * 24 * 3600  # Generate new orders every 7 days (keeping for backward compatibility)
        self.initialized = False  # Flag to track if initial orders have been generated

    def set_game_window(self, game_window):
        """Set reference to game window for accessing farm tiles"""
        self.game_window = game_window

    def generate_random_order(self):
        """Generate a random crop order"""
        # Select random crop from available seeds
        crop = random.choice(seeds_config)
        crop_name = crop['name']

        # Gradually increase order quantities as days pass
        # Day 1: 10-100 units (base range)
        # Day 10: 100-2000 units (moderate scaling)
        # Day 30: 1000-5000 units (continued growth)
        # Day 50+: 5000-9000 units (maximum scaling)
        current_day = max(1, self.market.current_day)  # Ensure day is at least 1
        
        if current_day <= 20:
            # Very early game: 10-100 to 100-2000 (over 9 days)
            min_quantity = 10 + (current_day - 1) * 10
            max_quantity = 100 + (current_day - 1) * 211.111
        elif current_day <= 50:
            # Early-mid game: 100-2000 to 1000-5000 (over 20 days)
            min_quantity = 100 + (current_day - 10) * 45
            max_quantity = 2000 + (current_day - 10) * 150
        elif current_day <= 100:
            # Mid-late game: 1000-5000 to 5000-9000 (over 20 days)
            min_quantity = 1000 + (current_day - 30) * 200
            max_quantity = 5000 + (current_day - 30) * 200
        else:
            # Late game: 5000-9000 (maximum scaling)
            min_quantity = 5000
            max_quantity = 9000
        
        # Ensure we don't go below minimums or exceed reasonable maximums
        min_quantity = max(10, int(min_quantity))
        max_quantity = max(min_quantity, min(9000, int(max_quantity)))
        
        quantity = random.randint(min_quantity, max_quantity)

        # Get current market price for this crop
        market_price = self.market.prices.get(crop_name, 10)  # Default to 10 if not found

        # Premium price (100%-500% of market price)
        premium_multiplier = random.uniform(1.0, 5.0)
        premium_price = market_price * premium_multiplier

        # Random duration (30-180 days)
        duration_days = random.randint(30, 180)

        return Order(crop_name, quantity, premium_price, duration_days, self.market.current_day)

    def initialize_starting_orders(self, market):
        """Initialize 4 starting orders - called after market is available"""
        if not self.initialized:
            self.market = market  # Store market reference

            # Create specific carrot order: 50 carrots for $10 each
            carrot_order = Order("Carrot", 50, 10.0, 90, market.current_day)  # 90 days duration
            self.incoming_orders.append(carrot_order)
            print(f"🎯 Created special starting order: 50 Carrots for $10.00 each (90 days)")

            # Generate 3 random orders
            for _ in range(3):
                order = self.generate_random_order()
                self.incoming_orders.append(order)
            self.initialized = True

    def update(self):
        """Update order system - generate new orders daily, cancel old unaccepted orders"""
        current_time = time.time()

        # Check if we have access to market day tracking
        if hasattr(self, 'market') and hasattr(self.market, 'current_day'):
            current_day = self.market.current_day

            # If this is a new day, generate 3 new orders and cancel old unaccepted orders
            if current_day != self.last_day_processed:
                # Generate 3 new orders every day
                for _ in range(3):
                    order = self.generate_random_order()
                    self.incoming_orders.append(order)
                print(f"📦 Generated 3 new crop orders for day {current_day}")

                # Cancel unaccepted orders that are 3 days old
                orders_to_cancel = []
                for order in self.incoming_orders:
                    order_age_days = current_day - order.created_day
                    if order_age_days >= 3:
                        orders_to_cancel.append(order)

                if orders_to_cancel:
                    for order in orders_to_cancel:
                        self.incoming_orders.remove(order)
                    print(f"🗑️ Cancelled {len(orders_to_cancel)} unaccepted orders that were 3+ days old")

                self.last_day_processed = current_day
        else:
            # Fallback to time-based generation (every 7 days, 1-3 orders) if market day tracking not available
            if current_time - self.last_order_generation >= self.order_generation_interval:
                # Generate 1-3 new orders
                num_orders = random.randint(1, 3)
                for _ in range(num_orders):
                    order = self.generate_random_order()
                    self.incoming_orders.append(order)
                self.last_order_generation = current_time

        # Remove expired orders (both incoming and accepted)
        current_day = self.market.current_day if hasattr(self, 'market') and self.market else 0
        expired_incoming = [order for order in self.incoming_orders if order.is_expired(current_day)]
        expired_accepted = [order for order in self.accepted_orders if order.is_expired(current_day)]

        if expired_incoming:
            self.incoming_orders = [order for order in self.incoming_orders if not order.is_expired(current_day)]
            print(f"⏰ {len(expired_incoming)} incoming orders expired")

        if expired_accepted:
            self.accepted_orders = [order for order in self.accepted_orders if not order.is_expired(current_day)]
            print(f"⏰ {len(expired_accepted)} accepted orders expired")

    def accept_order(self, order):
        """Accept an incoming order"""
        if order in self.incoming_orders:
            self.incoming_orders.remove(order)
            order.accepted = True
            self.accepted_orders.append(order)

    def reject_order(self, order):
        """Reject an incoming order"""
        if order in self.incoming_orders:
            self.incoming_orders.remove(order)

    def cancel_order(self, order):
        """Cancel an accepted order"""
        if order in self.accepted_orders:
            self.accepted_orders.remove(order)
            return True
        return False

    def fulfill_orders(self):
        """Attempt to fulfill accepted orders from barn storage every 30 seconds"""
        for order in self.accepted_orders[:]:  # Copy list to avoid modification during iteration
            if order.is_complete():
                continue

            crop_name = order.crop_name
            remaining_quantity = order.get_remaining_quantity()

            # Check if we have this crop in storage
            available_quantity = self.get_total_barn_storage(crop_name)

            if available_quantity > 0:
                # Fulfill as much as possible
                fulfill_amount = min(remaining_quantity, available_quantity)

                # Remove from barn storage
                self.remove_crops_from_barns(crop_name, fulfill_amount)

                # Fulfill the order
                order.fulfill(fulfill_amount)

                # Pay the premium price (1-5 times current market price)
                current_market_price = self.market.prices.get(crop_name, 10)
                premium_multiplier = random.uniform(1.0, 5.0)
                payment_per_unit = current_market_price * premium_multiplier
                total_payment = fulfill_amount * payment_per_unit
                self.game_state.finance.add_transaction(
                    TransactionType.CROP_SALE,
                    total_payment,
                    f"Fulfilled order: {fulfill_amount}x {crop_name} at ${payment_per_unit:.2f}/unit (premium bonus)"
                )
                # Update game_state.money to match finance.current_money
                self.game_state.money = self.game_state.finance.get_balance()
                
                # Gain prestige from order revenue
                self.game_state.gain_prestige_from_orders(total_payment)

                # Update UI info window immediately after transaction
                if hasattr(self.game_window, 'ui_info_window'):
                    try:
                        self.game_window.ui_info_window._update_info()
                    except Exception as e:
                        print(f"Warning: Could not update UI info window after automatic order fulfillment: {e}")

                # Remove completed orders
                if order.is_complete():
                    self.accepted_orders.remove(order)

    def complete_order(self, order):
        """Manually complete an accepted order by instantly fulfilling it at premium price"""
        if order not in self.accepted_orders:
            return False

        remaining_quantity = order.get_remaining_quantity()
        crop_name = order.crop_name

        # Check if player has enough crops in storage
        available_quantity = self.get_total_barn_storage(crop_name)
        if available_quantity < remaining_quantity:
            return False  # Not enough crops in storage

        # Remove crops from barn storage
        self.remove_crops_from_barns(crop_name, remaining_quantity)

        # Pay the order's premium price (the price that was offered)
        total_payment = remaining_quantity * order.premium_price
        self.game_state.finance.add_transaction(
            TransactionType.CROP_SALE,
            total_payment,
            f"Instant order completion: {remaining_quantity}x {crop_name} at ${order.premium_price:.2f}/unit (order premium)"
        )
        # Update game_state.money to match finance.current_money
        self.game_state.money = self.game_state.finance.get_balance()
        
        # Gain prestige from order revenue
        self.game_state.gain_prestige_from_orders(total_payment)

        # Update UI info window immediately after transaction
        if hasattr(self.game_window, 'ui_info_window'):
            try:
                self.game_window.ui_info_window._update_info()
            except Exception as e:
                print(f"Warning: Could not update UI info window after manual order completion: {e}")

        # Mark order as complete
        order.fulfilled_quantity = order.quantity

        # Remove from accepted orders
        self.accepted_orders.remove(order)
        return True

    def remove_crops_from_barns(self, crop_name, amount_to_remove):
        """Remove specified amount of crops from barn tiles"""
        if not self.game_window:
            return
        
        remaining_to_remove = amount_to_remove
        for tile in self.game_window.farm_tiles:
            if tile.state == 6 and tile.stored_crop_type == crop_name and remaining_to_remove > 0:  # TILE_BARN
                _, removed = tile.remove_crop(remaining_to_remove)
                remaining_to_remove -= removed
                if remaining_to_remove <= 0:
                    break

    def get_total_barn_storage(self, crop_name):
        """Get total amount of a crop stored across all barn tiles"""
        if not self.game_window:
            return 0
        
        total = 0
        for tile in self.game_window.farm_tiles:
            if tile.state == 6:  # TILE_BARN
                if tile.stored_crop_type == crop_name:
                    total += tile.stored_amount
        return total

    def get_incoming_orders(self):
        """Get orders that haven't been accepted yet"""
        return self.incoming_orders

    def get_accepted_orders(self):
        """Get orders that have been accepted"""
        return self.accepted_orders
    
    def save_order_data(self):
        """Save order system data for game saving"""
        incoming_data = []
        for order in self.incoming_orders:
            order_data = {
                'crop_name': order.crop_name,
                'quantity': order.quantity,
                'premium_price': order.premium_price,
                'duration_days': order.duration_days,
                'created_day': order.created_day,
                'accepted': order.accepted,
                'fulfilled_quantity': order.fulfilled_quantity
            }
            incoming_data.append(order_data)
        
        accepted_data = []
        for order in self.accepted_orders:
            order_data = {
                'crop_name': order.crop_name,
                'quantity': order.quantity,
                'premium_price': order.premium_price,
                'duration_days': order.duration_days,
                'created_day': order.created_day,
                'accepted': order.accepted,
                'fulfilled_quantity': order.fulfilled_quantity
            }
            accepted_data.append(order_data)
        
        return {
            'incoming_orders': incoming_data,
            'accepted_orders': accepted_data,
            'last_order_generation': self.last_order_generation
        }
    
    def load_order_data(self, order_data):
        """Load order system data from saved game"""
        # Clear existing orders
        self.incoming_orders = []
        self.accepted_orders = []
        
        # Load incoming orders
        if 'incoming_orders' in order_data:
            for order_dict in order_data['incoming_orders']:
                order = Order(
                    order_dict['crop_name'],
                    order_dict['quantity'],
                    order_dict['premium_price'],
                    order_dict['duration_days'],
                    order_dict.get('created_day', 0)
                )
                order.accepted = order_dict.get('accepted', False)
                order.fulfilled_quantity = order_dict.get('fulfilled_quantity', 0)
                self.incoming_orders.append(order)
        
        # Load accepted orders
        if 'accepted_orders' in order_data:
            for order_dict in order_data['accepted_orders']:
                order = Order(
                    order_dict['crop_name'],
                    order_dict['quantity'],
                    order_dict['premium_price'],
                    order_dict['duration_days'],
                    order_dict.get('created_day', 0)
                )
                order.accepted = order_dict.get('accepted', True)
                order.fulfilled_quantity = order_dict.get('fulfilled_quantity', 0)
                self.accepted_orders.append(order)
        
        # Load last order generation time
        if 'last_order_generation' in order_data:
            self.last_order_generation = order_data['last_order_generation']

