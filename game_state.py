from constants import game_config, seeds_config, fertilizer_config
from finance import Finance, TransactionType
from order_system import OrderSystem


class GameState:
    def __init__(self):
        # Initialize finance system with appropriate starting money based on gamemode
        starting_money = 100000 if game_config.get('gamemode') == 'DEBUG' else 1000
        self.finance = Finance(starting_money=starting_money)
        self.money = self.finance.get_balance()  # Money is now managed by finance system
        
        self.barn_capacity = game_config['barn_max_capacity']
        self.barn_storage = {}  # Crop storage
        self.seed_inventory = {}  # Seeds inventory
        self.fertilizer_inventory = {}  # Fertilizer inventory
        self.selected_seed = None
        self.selected_fertilizer = None
        self.tractor_row_mode = 1  # Default to 1-row mode
        self.tractor_3_row_purchased = False  # Track if 3-row upgrade is purchased
        self.prestige = 250 if game_config.get('gamemode') == 'DEBUG' else 1  # Player prestige level
        self.total_order_revenue = 0  # Cumulative order revenue for prestige calculation
        
        # Initialize seed inventory (empty - seeds are now stored in buildings)
        for seed in seeds_config:
            self.seed_inventory[seed['name']] = 0  # No starting seeds
            
        # Initialize fertilizer inventory
        for fertilizer in fertilizer_config:
            self.fertilizer_inventory[fertilizer['name']] = 5  # Start with 5 of each fertilizer
        
        # Initialize order system
        self.order_system = OrderSystem(self)
        
        # Try to load existing finance data
        self.load_finance_data()
    
    def can_afford(self, cost):
        return self.finance.can_afford(cost)
    
    def spend_money(self, amount, transaction_type=None, description="", metadata=None):
        """Spend money with automatic transaction tracking"""
        # Auto-detect transaction type if not provided
        if transaction_type is None:
            transaction_type = TransactionType.TILE_PURCHASE  # Default fallback
        
        success = self.finance.spend_money(amount, transaction_type, description, metadata)
        if success:
            self.money = self.finance.get_balance()  # Update local money reference
        return success
    
    def earn_money(self, amount, transaction_type=None, description="", metadata=None):
        """Earn money with automatic transaction tracking"""
        if transaction_type is None:
            transaction_type = TransactionType.CROP_SALE  # Default for earning money
        
        self.finance.earn_money(amount, transaction_type, description, metadata)
        self.money = self.finance.get_balance()  # Update local money reference
    
    def add_to_barn(self, crop_name, amount):
        current_total = sum(self.barn_storage.values())
        if current_total + amount <= self.barn_capacity:
            if crop_name in self.barn_storage:
                self.barn_storage[crop_name] += amount
            else:
                self.barn_storage[crop_name] = amount
            return True
        return False
    
    def buy_seed(self, seed_name):
        for seed in seeds_config:
            if seed['name'] == seed_name and self.can_afford(seed['cost']):
                if self.spend_money(seed['cost'], TransactionType.SEED_PURCHASE, 
                                  f"Purchased {seed_name} seed", {'seed_type': seed_name}):
                    if seed_name in self.seed_inventory:
                        self.seed_inventory[seed_name] += 1
                    else:
                        self.seed_inventory[seed_name] = 1
                    return True
        return False
    
    def use_seed(self, seed_name):
        if seed_name in self.seed_inventory and self.seed_inventory[seed_name] > 0:
            self.seed_inventory[seed_name] -= 1
            return True
        return False
    
    def get_financial_report(self):
        """Get comprehensive financial report"""
        return self.finance.get_financial_report()
    
    def get_spending_by_category(self):
        """Get spending breakdown by category"""
        return self.finance.get_spending_by_category()
    
    def get_recent_transactions(self, count=10):
        """Get recent transactions"""
        return self.finance.get_recent_transactions(count)
    
    def print_financial_summary(self):
        """Print formatted financial summary"""
        self.finance.print_summary()
    
    def save_finance_data(self, filename="finance_data.json"):
        """Save financial data to file"""
        return self.finance.save_to_file(filename)
    
    def load_finance_data(self, filename="finance_data.json"):
        """Load financial data from file"""
        if self.finance.load_from_file(filename):
            self.money = self.finance.get_balance()  # Update local money reference
            return True
        return False
    
    def gain_prestige_from_orders(self, revenue_amount):
        """Gain prestige based on cumulative order revenue (1 prestige per $750)"""
        # Add to cumulative total
        self.total_order_revenue += revenue_amount
        
        # Calculate how many $750 thresholds we've crossed
        prestige_gained = int(self.total_order_revenue // 750) - int((self.total_order_revenue - revenue_amount) // 750)
        
        if prestige_gained > 0:
            self.prestige += prestige_gained
            print(f"🎖️ Gained {prestige_gained} prestige from ${revenue_amount:.2f} order revenue! (Total: ${self.total_order_revenue:.2f})")
            return prestige_gained
        return 0
    
    def save_game_state(self, filename="game_save.json"):
        """Save complete game state to file"""
        import json
        try:
            game_data = {
                'money': self.money,
                'barn_capacity': self.barn_capacity,
                'barn_storage': self.barn_storage,
                'seed_inventory': self.seed_inventory,
                'fertilizer_inventory': self.fertilizer_inventory,
                'selected_seed': self.selected_seed,
                'selected_fertilizer': self.selected_fertilizer,
                'tractor_row_mode': self.tractor_row_mode,
                'tractor_3_row_purchased': self.tractor_3_row_purchased,
                'prestige': self.prestige,
                'total_order_revenue': self.total_order_revenue
            }
            
            with open(filename, 'w') as f:
                json.dump(game_data, f, indent=2)
            
            print(f"💾 Game state saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Failed to save game state: {e}")
            return False
    
    def load_game_state(self, filename="game_save.json"):
        """Load complete game state from file"""
        import json
        try:
            with open(filename, 'r') as f:
                game_data = json.load(f)
            
            self.money = game_data.get('money', self.money)
            self.barn_capacity = game_data.get('barn_capacity', self.barn_capacity)
            self.barn_storage = game_data.get('barn_storage', {})
            self.seed_inventory = game_data.get('seed_inventory', {})
            self.fertilizer_inventory = game_data.get('fertilizer_inventory', {})
            self.selected_seed = game_data.get('selected_seed', self.selected_seed)
            self.selected_fertilizer = game_data.get('selected_fertilizer', self.selected_fertilizer)
            self.tractor_row_mode = game_data.get('tractor_row_mode', self.tractor_row_mode)
            self.tractor_3_row_purchased = game_data.get('tractor_3_row_purchased', self.tractor_3_row_purchased)
            self.prestige = game_data.get('prestige', self.prestige)
            self.total_order_revenue = game_data.get('total_order_revenue', 0)
            
            # Update finance system balance
            self.finance.current_money = self.money
            
            print(f"📂 Game state loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"📂 No save file found at {filename}")
            return False
        except Exception as e:
            print(f"❌ Failed to load game state: {e}")
            return False

