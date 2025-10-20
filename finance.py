"""
Finance System - Tracks all spending and income in the game
"""
import json
import time
from datetime import datetime
from collections import defaultdict


class TransactionType:
    # Income types
    CROP_SALE = "crop_sale"
    INITIAL_MONEY = "initial_money"
    
    # Expense types
    TILE_PURCHASE = "tile_purchase"
    SEED_PURCHASE = "seed_purchase"
    FERTILIZER_PURCHASE = "fertilizer_purchase"
    BUILDING_CONSTRUCTION = "building_construction"
    TRACTOR_UPGRADE = "tractor_upgrade"


class Transaction:
    """Represents a single financial transaction"""
    
    def __init__(self, transaction_type, amount, description="", metadata=None):
        self.timestamp = time.time()
        self.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_type = transaction_type
        self.amount = amount  # Positive for income, negative for expenses
        self.description = description
        self.metadata = metadata or {}  # Additional data (crop type, location, etc.)
        
    def to_dict(self):
        """Convert transaction to dictionary for saving"""
        return {
            'timestamp': self.timestamp,
            'datetime': self.datetime,
            'type': self.transaction_type,
            'amount': self.amount,
            'description': self.description,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create transaction from dictionary"""
        transaction = cls(
            data['type'],
            data['amount'],
            data.get('description', ''),
            data.get('metadata', {})
        )
        transaction.timestamp = data['timestamp']
        transaction.datetime = data['datetime']
        return transaction


class Finance:
    """Main finance tracking system"""
    
    def __init__(self, starting_money=1000):
        self.starting_money = starting_money
        self.current_money = 0  # Start at 0, will be set by initial transaction
        self.transactions = []
        self.daily_stats = defaultdict(lambda: {'income': 0, 'expenses': 0})
        
        # Track spending by category
        self.category_totals = defaultdict(float)
        
        # Record initial money
        self.add_transaction(TransactionType.INITIAL_MONEY, starting_money, "Starting funds")
        
    def add_transaction(self, transaction_type, amount, description="", metadata=None):
        """Add a new transaction and update balances"""
        transaction = Transaction(transaction_type, amount, description, metadata)
        self.transactions.append(transaction)
        
        # Update current money
        self.current_money += amount
        
        # Update category totals
        self.category_totals[transaction_type] += abs(amount)
        
        # Update daily stats
        date_key = datetime.fromtimestamp(transaction.timestamp).strftime("%Y-%m-%d")
        if amount > 0:
            self.daily_stats[date_key]['income'] += amount
        else:
            self.daily_stats[date_key]['expenses'] += abs(amount)
            
        return transaction
    
    def can_afford(self, cost):
        """Check if we can afford a purchase"""
        return self.current_money >= cost
    
    def spend_money(self, amount, transaction_type, description="", metadata=None):
        """Spend money and record transaction"""
        if self.can_afford(amount):
            self.add_transaction(transaction_type, -amount, description, metadata)
            return True
        return False
    
    def earn_money(self, amount, transaction_type, description="", metadata=None):
        """Earn money and record transaction"""
        self.add_transaction(transaction_type, amount, description, metadata)
        return True
    
    def get_balance(self):
        """Get current money balance"""
        return self.current_money
    
    def get_total_income(self):
        """Get total income earned"""
        return sum(t.amount for t in self.transactions if t.amount > 0)
    
    def get_total_expenses(self):
        """Get total expenses (as positive number)"""
        return sum(abs(t.amount) for t in self.transactions if t.amount < 0)
    
    def get_net_profit(self):
        """Get net profit/loss"""
        return self.get_total_income() - self.get_total_expenses()
    
    def get_transactions_by_type(self, transaction_type):
        """Get all transactions of a specific type"""
        return [t for t in self.transactions if t.transaction_type == transaction_type]
    
    def get_spending_by_category(self):
        """Get spending breakdown by category"""
        spending = {}
        for transaction in self.transactions:
            if transaction.amount < 0:  # Only expenses
                category = transaction.transaction_type
                if category not in spending:
                    spending[category] = 0
                spending[category] += abs(transaction.amount)
        return spending
    
    def get_recent_transactions(self, count=10):
        """Get most recent transactions"""
        return self.transactions[-count:] if len(self.transactions) >= count else self.transactions
    
    def get_daily_summary(self, date=None):
        """Get financial summary for a specific date (default: today)"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        return self.daily_stats.get(date, {'income': 0, 'expenses': 0})
    
    def get_financial_report(self):
        """Generate a comprehensive financial report"""
        report = {
            'current_balance': self.current_money,
            'starting_money': self.starting_money,
            'total_income': self.get_total_income(),
            'total_expenses': self.get_total_expenses(),
            'net_profit': self.get_net_profit(),
            'spending_by_category': self.get_spending_by_category(),
            'transaction_count': len(self.transactions),
            'recent_transactions': [t.to_dict() for t in self.get_recent_transactions(5)]
        }
        return report
    
    def save_to_file(self, filename="finance_data.json"):
        """Save financial data to file"""
        data = {
            'starting_money': self.starting_money,
            'current_money': self.current_money,
            'transactions': [t.to_dict() for t in self.transactions],
            'created': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving finance data: {e}")
            return False
    
    def load_from_file(self, filename="finance_data.json"):
        """Load financial data from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.starting_money = data.get('starting_money', 1000)
            self.current_money = data.get('current_money', self.starting_money)
            
            # Load transactions
            self.transactions = []
            for t_data in data.get('transactions', []):
                self.transactions.append(Transaction.from_dict(t_data))
            
            # Rebuild category totals and daily stats
            self.category_totals = defaultdict(float)
            self.daily_stats = defaultdict(lambda: {'income': 0, 'expenses': 0})
            
            for transaction in self.transactions:
                self.category_totals[transaction.transaction_type] += abs(transaction.amount)
                date_key = datetime.fromtimestamp(transaction.timestamp).strftime("%Y-%m-%d")
                if transaction.amount > 0:
                    self.daily_stats[date_key]['income'] += transaction.amount
                else:
                    self.daily_stats[date_key]['expenses'] += abs(transaction.amount)
            
            return True
        except FileNotFoundError:
            print(f"Finance file {filename} not found, starting with fresh data")
            return False
        except Exception as e:
            print(f"Error loading finance data: {e}")
            return False
    
    def print_summary(self):
        """Print a formatted financial summary"""
        report = self.get_financial_report()
        
        print("="*50)
        print("FINANCIAL SUMMARY")
        print("="*50)
        print(f"Current Balance: ${report['current_balance']:.2f}")
        print(f"Starting Money:  ${report['starting_money']:.2f}")
        print(f"Total Income:    ${report['total_income']:.2f}")
        print(f"Total Expenses:  ${report['total_expenses']:.2f}")
        print(f"Net Profit:      ${report['net_profit']:.2f}")
        print(f"Transactions:    {report['transaction_count']}")
        
        print("\nSPENDING BY CATEGORY:")
        print("-" * 30)
        for category, amount in sorted(report['spending_by_category'].items()):
            print(f"{category.replace('_', ' ').title():<20} ${amount:.2f}")
        
        print("\nRECENT TRANSACTIONS:")
        print("-" * 30)
        for t in report['recent_transactions']:
            amount_str = f"${abs(t['amount']):.2f}"
            sign = "+" if t['amount'] > 0 else "-"
            print(f"{t['datetime'][:16]} {sign}{amount_str:<8} {t['description']}")

