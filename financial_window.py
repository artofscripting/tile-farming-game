"""
Financial Summary Window - Displays comprehensive financial information
"""
import tkinter as tk
from tkinter import ttk
import threading
import time


class FinancialSummaryWindow:
    """Separate window for displaying detailed financial information"""
    
    def __init__(self, game_window):
        self.game_window = game_window
        self.root = None
        self.running = False
        self.labels = {}
        self.transaction_text = None
        self.category_text = None
        
    def create_window(self):
        """Create the financial summary window"""
        if self.root:
            return
            
        self.root = tk.Toplevel()
        self.root.title("Financial Summary")
        # Set width to 750 and height to match game window height
        game_height = self.game_window.height
        self.root.geometry(f"750x{game_height}")
        self.root.configure(bg='#1a1a1a')
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Make window stay on top initially
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        
        # Create centered container
        container = tk.Frame(self.root, bg='#1a1a1a')
        container.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Main frame with scrollbar inside the container
        main_canvas = tk.Canvas(container, bg='#1a1a1a', highlightthickness=0)
        main_scrollbar = ttk.Scrollbar(container, orient="vertical", command=main_canvas.yview)
        self.main_frame = tk.Frame(main_canvas, bg='#1a1a1a')
        
        self.main_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")
        
        self._create_widgets()
        self._start_update_loop()
    
    def _create_widgets(self):
        """Create all the UI widgets"""
        # Title - centered
        title_label = tk.Label(self.main_frame, text="FINANCIAL SUMMARY", 
                              fg='gold', bg='#1a1a1a', font=('Arial', 16, 'bold'))
        title_label.pack(pady=10, anchor='center')
        
        # Current Status Section - centered
        status_frame = tk.Frame(self.main_frame, bg='#2a2a2a', relief='raised', bd=2)
        status_frame.pack(fill='x', padx=20, pady=5, anchor='center')
        
        tk.Label(status_frame, text="CURRENT STATUS", 
                fg='lightblue', bg='#2a2a2a', font=('Arial', 12, 'bold')).pack(pady=5, anchor='center')
        
        self.labels['current_money'] = tk.Label(status_frame, text="Current Balance: $0", 
                                               fg='white', bg='#2a2a2a', font=('Arial', 11))
        self.labels['current_money'].pack(anchor='w', padx=10, pady=2)
        
        self.labels['net_worth'] = tk.Label(status_frame, text="Net Worth: $0", 
                                           fg='yellow', bg='#2a2a2a', font=('Arial', 11, 'bold'))
        self.labels['net_worth'].pack(anchor='w', padx=10, pady=2)
        
        # Financial Summary Section - centered
        summary_frame = tk.Frame(self.main_frame, bg='#2a2a2a', relief='raised', bd=2)
        summary_frame.pack(fill='x', padx=20, pady=5, anchor='center')
        
        tk.Label(summary_frame, text="FINANCIAL OVERVIEW", 
                fg='lightgreen', bg='#2a2a2a', font=('Arial', 12, 'bold')).pack(pady=5, anchor='center')
        
        self.labels['total_income'] = tk.Label(summary_frame, text="Total Income: $0", 
                                              fg='lightgreen', bg='#2a2a2a', font=('Arial', 10))
        self.labels['total_income'].pack(anchor='w', padx=10, pady=1)
        
        self.labels['total_expenses'] = tk.Label(summary_frame, text="Total Expenses: $0", 
                                                fg='lightcoral', bg='#2a2a2a', font=('Arial', 10))
        self.labels['total_expenses'].pack(anchor='w', padx=10, pady=1)
        
        self.labels['net_profit'] = tk.Label(summary_frame, text="Net Profit: $0", 
                                            fg='white', bg='#2a2a2a', font=('Arial', 10, 'bold'))
        self.labels['net_profit'].pack(anchor='w', padx=10, pady=1)
        
        self.labels['transaction_count'] = tk.Label(summary_frame, text="Transactions: 0", 
                                                   fg='lightgray', bg='#2a2a2a', font=('Arial', 10))
        self.labels['transaction_count'].pack(anchor='w', padx=10, pady=1)
        
        # Net Worth Breakdown Section - centered
        networth_frame = tk.Frame(self.main_frame, bg='#2a2a2a', relief='raised', bd=2)
        networth_frame.pack(fill='x', padx=20, pady=5, anchor='center')
        
        tk.Label(networth_frame, text="NET WORTH BREAKDOWN", 
                fg='gold', bg='#2a2a2a', font=('Arial', 12, 'bold')).pack(pady=5, anchor='center')
        
        self.labels['cash_value'] = tk.Label(networth_frame, text="Cash: $0", 
                                            fg='white', bg='#2a2a2a', font=('Arial', 10))
        self.labels['cash_value'].pack(anchor='w', padx=10, pady=1)
        
        self.labels['inventory_value'] = tk.Label(networth_frame, text="Inventory Value: $0", 
                                                 fg='lightblue', bg='#2a2a2a', font=('Arial', 10))
        self.labels['inventory_value'].pack(anchor='w', padx=10, pady=1)
        
        self.labels['assets_value'] = tk.Label(networth_frame, text="Assets Value: $0", 
                                              fg='lightgreen', bg='#2a2a2a', font=('Arial', 10))
        self.labels['assets_value'].pack(anchor='w', padx=10, pady=1)
        
        # Spending Categories Section - centered
        categories_frame = tk.Frame(self.main_frame, bg='#2a2a2a', relief='raised', bd=2)
        categories_frame.pack(fill='both', expand=True, padx=20, pady=5, anchor='center')
        
        tk.Label(categories_frame, text="SPENDING BY CATEGORY", 
                fg='orange', bg='#2a2a2a', font=('Arial', 12, 'bold')).pack(pady=5, anchor='center')
        
        # Scrollable text widget for spending categories
        category_frame = tk.Frame(categories_frame, bg='#2a2a2a')
        category_frame.pack(fill='both', expand=True, pady=5, padx=10)
        
        self.category_text = tk.Text(category_frame, height=8, width=75, 
                                    bg='#3a3a3a', fg='lightgray', font=('Arial', 9))
        category_scrollbar = tk.Scrollbar(category_frame, orient="vertical", 
                                         command=self.category_text.yview)
        self.category_text.configure(yscrollcommand=category_scrollbar.set)
        
        self.category_text.pack(side='left', fill='both', expand=True)
        category_scrollbar.pack(side='right', fill='y')
        
        # Recent Transactions Section - centered
        transactions_frame = tk.Frame(self.main_frame, bg='#2a2a2a', relief='raised', bd=2)
        transactions_frame.pack(fill='both', expand=True, padx=20, pady=5, anchor='center')
        
        tk.Label(transactions_frame, text="RECENT TRANSACTIONS", 
                fg='cyan', bg='#2a2a2a', font=('Arial', 12, 'bold')).pack(pady=5, anchor='center')
        
        # Scrollable text widget for recent transactions
        transaction_frame = tk.Frame(transactions_frame, bg='#2a2a2a')
        transaction_frame.pack(fill='both', expand=True, pady=5, padx=10)
        
        self.transaction_text = tk.Text(transaction_frame, height=20, width=75, 
                                       bg='#3a3a3a', fg='lightgray', font=('Arial', 9))
        transaction_scrollbar = tk.Scrollbar(transaction_frame, orient="vertical", 
                                            command=self.transaction_text.yview)
        self.transaction_text.configure(yscrollcommand=transaction_scrollbar.set)
        
        self.transaction_text.pack(side='left', fill='both', expand=True)
        transaction_scrollbar.pack(side='right', fill='y')
    
    def _calculate_net_worth(self):
        """Calculate total net worth including cash, inventory, and assets"""
        try:
            # Cash value (current money)
            cash_value = self.game_window.game_state.money
            
            # Inventory value (crops in barns + seeds)
            inventory_value = 0
            
            # Calculate crop value in barns
            if hasattr(self.game_window, 'market'):
                for crop_name, amount in self.game_window.game_state.barn_storage.items():
                    market_price = self.game_window.market.get_price(crop_name)
                    inventory_value += market_price * amount
            
            # Calculate seed inventory value (assume seeds cost same as their market price)
            for seed_name, amount in self.game_window.game_state.seed_inventory.items():
                if hasattr(self.game_window, 'market'):
                    seed_price = self.game_window.market.get_price(seed_name)
                    inventory_value += seed_price * amount
            
            # Assets value (buildings, upgrades, etc.)
            assets_value = 0
            
            # Count buildings (approximate values)
            if hasattr(self.game_window, 'farm_tiles'):
                barn_count = sum(1 for tile in self.game_window.farm_tiles if hasattr(tile, 'state') and tile.state == 6)  # TILE_BARN
                seed_bin_count = sum(1 for tile in self.game_window.farm_tiles if hasattr(tile, 'state') and tile.state == 5)  # TILE_SEED_BIN
                
                assets_value += barn_count * 200  # Barn cost
                assets_value += seed_bin_count * 100  # Seed bin cost
            
            # Add tractor upgrades value
            if self.game_window.game_state.tractor_3_row_purchased:
                assets_value += 500  # 3-row upgrade cost
            
            return cash_value, inventory_value, assets_value, cash_value + inventory_value + assets_value
            
        except Exception as e:
            return 0, 0, 0, 0
    
    def _update_info(self):
        """Update all financial information"""
        if not self.running or not self.root:
            return
            
        try:
            if hasattr(self.game_window.game_state, 'finance'):
                finance = self.game_window.game_state.finance
                
                # Basic financial info
                current_money = finance.get_balance()
                total_income = finance.get_total_income()
                total_expenses = finance.get_total_expenses()
                net_profit = finance.get_net_profit()
                transaction_count = len(finance.transactions)
                
                # Calculate net worth
                cash_value, inventory_value, assets_value, total_net_worth = self._calculate_net_worth()
                
                # Update current status labels
                self.labels['current_money'].config(text=f"Current Balance: ${current_money:.2f}")
                self.labels['net_worth'].config(text=f"Net Worth: ${total_net_worth:.2f}")
                
                # Update financial overview
                self.labels['total_income'].config(text=f"Total Income: ${total_income:.2f}")
                self.labels['total_expenses'].config(text=f"Total Expenses: ${total_expenses:.2f}")
                
                # Color net profit based on positive/negative
                profit_color = 'lightgreen' if net_profit >= 0 else 'lightcoral'
                self.labels['net_profit'].config(text=f"Net Profit: ${net_profit:.2f}", fg=profit_color)
                self.labels['transaction_count'].config(text=f"Transactions: {transaction_count}")
                
                # Update net worth breakdown
                self.labels['cash_value'].config(text=f"Cash: ${cash_value:.2f}")
                self.labels['inventory_value'].config(text=f"Inventory Value: ${inventory_value:.2f}")
                self.labels['assets_value'].config(text=f"Assets Value: ${assets_value:.2f}")
                
                # Update spending categories
                self.category_text.delete(1.0, tk.END)
                spending_by_category = finance.get_spending_by_category()
                if spending_by_category:
                    for category, amount in sorted(spending_by_category.items(), key=lambda x: x[1], reverse=True):
                        category_name = category.replace('_', ' ').title()
                        percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                        self.category_text.insert(tk.END, f"{category_name:<20} ${amount:>8.2f} ({percentage:>5.1f}%)\n")
                else:
                    self.category_text.insert(tk.END, "No expenses recorded yet")
                
                # Update recent transactions
                self.transaction_text.delete(1.0, tk.END)
                recent_transactions = finance.get_recent_transactions(15)
                if recent_transactions:
                    for transaction in reversed(recent_transactions):  # Show newest first
                        sign = "+" if transaction.amount > 0 else "-"
                        amount_str = f"${abs(transaction.amount):>7.2f}"
                        date_str = transaction.datetime[:16]  # Just date and time
                        
                        # Color code based on transaction type
                        if transaction.amount > 0:
                            color_tag = "income"
                        else:
                            color_tag = "expense"
                        
                        line = f"{date_str} {sign}{amount_str} {transaction.description}\n"
                        self.transaction_text.insert(tk.END, line)
                    
                    # Configure text colors
                    self.transaction_text.tag_configure("income", foreground="lightgreen")
                    self.transaction_text.tag_configure("expense", foreground="lightcoral")
                else:
                    self.transaction_text.insert(tk.END, "No transactions recorded yet")
                
            else:
                # Finance system not available
                for label in self.labels.values():
                    if hasattr(label, 'config'):
                        label.config(text="Finance system not available")
                        
        except Exception as e:
            pass  # Ignore errors during updates
    
    def _start_update_loop(self):
        """Start the update loop"""
        self.running = True
        self._update_loop()
    
    def _update_loop(self):
        """Update loop that runs every 500ms"""
        if self.running and self.root:
            self._update_info()
            self.root.after(500, self._update_loop)  # Update every 500ms
    

    
    def _on_close(self):
        """Handle window close"""
        self.running = False
        if self.root:
            self.root.destroy()
            self.root = None
    
    def show(self):
        """Show the financial summary window"""
        if not self.root:
            self.create_window()
        else:
            try:
                self.root.deiconify()
                self.root.lift()
            except Exception:
                # If tkinter operations fail, recreate the window
                self.root = None
                self.create_window()
    
    def hide(self):
        """Hide the financial summary window"""
        if self.root:
            try:
                self.root.withdraw()
            except Exception:
                # If tkinter call fails, clear the reference
                self.root = None
    
    def is_visible(self):
        """Check if window is visible"""
        if self.root is None:
            return False
        
        try:
            return self.root.winfo_viewable()
        except Exception:
            # If tkinter call fails, assume window is not visible and clean up
            self.root = None
            return False

