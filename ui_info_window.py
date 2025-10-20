import tkinter as tk
from tkinter import ttk
import threading
from constants import TILE_BARN, TILE_SEED_BIN


class UIInfoWindow:
    """Separate window for displaying game UI information using tkinter"""
    
    def __init__(self, game_window):
        self.game_window = game_window
        self.root = None
        self.running = False
        
        # Start the tkinter window in a separate thread
        self.thread = threading.Thread(target=self._create_window, daemon=True)
        self.thread.start()
    
    def show(self):
        """Show the farm info window"""
        if self.root:
            try:
                self.root.deiconify()
                self.root.lift()
            except Exception:
                # If tkinter operations fail, window might be destroyed
                self.root = None
    
    def hide(self):
        """Hide the farm info window"""
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
    
    def _create_window(self):
        """Create the tkinter window"""
        self.root = tk.Tk()
        self.root.title("Farm Info")
        self.root.geometry("300x700")
        self.root.configure(bg='#2a2a2a')
        
        # Try to position window to the right of main window
        try:
            self.root.geometry(f"+{self.game_window.get_location()[0] + self.game_window.width + 10}+{self.game_window.get_location()[1]}")
        except:
            pass  # If positioning fails, use default
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Make window unclosable - disable close button
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)  # Do nothing on close attempt
        
        # Create a frame for all content
        self.main_frame = tk.Frame(self.root, bg='#2a2a2a')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create labels for various info
        self.labels = {}
        
        # Money
        self.labels['money'] = tk.Label(self.main_frame, text="Money: $0", 
                                       fg='white', bg='#2a2a2a', font=('Arial', 12))
        self.labels['money'].pack(anchor='w', pady=2)
        
        # Day
        self.labels['day'] = tk.Label(self.main_frame, text="Day 0 - Monday", 
                                     fg='white', bg='#2a2a2a', font=('Arial', 12))
        self.labels['day'].pack(anchor='w', pady=2)
        
        # Prestige
        self.labels['prestige'] = tk.Label(self.main_frame, text="Prestige: 1",
                                          fg='white', bg='#2a2a2a', font=('Arial', 12))
        self.labels['prestige'].pack(anchor='w', pady=2)        # Separator
        tk.Frame(self.main_frame, height=2, bg='gray').pack(fill='x', pady=10)
        
        # Barn info
        self.labels['barn_title'] = tk.Label(self.main_frame, text="BARN STORAGE", 
                                            fg='yellow', bg='#2a2a2a', font=('Arial', 12, 'bold'))
        self.labels['barn_title'].pack(anchor='w', pady=(5, 2))
        
        # Create scrollable text widget for barn contents
        barn_frame = tk.Frame(self.main_frame, bg='#2a2a2a')
        barn_frame.pack(fill='both', expand=True, pady=5)
        
        self.barn_text = tk.Text(barn_frame, height=8, width=30, 
                                bg='#3a3a3a', fg='lightgray', font=('Arial', 9))
        barn_scrollbar = tk.Scrollbar(barn_frame, orient="vertical", command=self.barn_text.yview)
        self.barn_text.configure(yscrollcommand=barn_scrollbar.set)
        
        self.barn_text.pack(side='left', fill='both', expand=True)
        barn_scrollbar.pack(side='right', fill='y')
        
        # Seeds info  
        self.labels['seeds_title'] = tk.Label(self.main_frame, text="SEED INVENTORY", 
                                             fg='lightgreen', bg='#2a2a2a', font=('Arial', 12, 'bold'))
        self.labels['seeds_title'].pack(anchor='w', pady=(10, 2))
        
        # Create scrollable text widget for seed inventory
        seeds_frame = tk.Frame(self.main_frame, bg='#2a2a2a')
        seeds_frame.pack(fill='both', expand=True, pady=5)
        
        self.seeds_text = tk.Text(seeds_frame, height=6, width=30, 
                                 bg='#3a3a3a', fg='lightgray', font=('Arial', 9))
        seeds_scrollbar = tk.Scrollbar(seeds_frame, orient="vertical", command=self.seeds_text.yview)
        self.seeds_text.configure(yscrollcommand=seeds_scrollbar.set)
        
        self.seeds_text.pack(side='left', fill='both', expand=True)
        seeds_scrollbar.pack(side='right', fill='y')
        
        # Tractor Queue info
        self.labels['queue_title'] = tk.Label(self.main_frame, text="TRACTOR QUEUE", 
                                             fg='orange', bg='#2a2a2a', font=('Arial', 12, 'bold'))
        self.labels['queue_title'].pack(anchor='w', pady=(10, 2))
        
        self.labels['queue_count'] = tk.Label(self.main_frame, text="Queue: 0 jobs", 
                                             fg='white', bg='#2a2a2a', font=('Arial', 10))
        self.labels['queue_count'].pack(anchor='w', pady=2)
        
        # Create scrollable text widget for queue contents
        queue_frame = tk.Frame(self.main_frame, bg='#2a2a2a')
        queue_frame.pack(fill='both', expand=True, pady=5)
        
        self.queue_text = tk.Text(queue_frame, height=8, width=30, 
                                 bg='#3a3a3a', fg='lightgray', font=('Arial', 9))
        queue_scrollbar = tk.Scrollbar(queue_frame, orient="vertical", command=self.queue_text.yview)
        self.queue_text.configure(yscrollcommand=queue_scrollbar.set)
        
        self.queue_text.pack(side='left', fill='both', expand=True)
        queue_scrollbar.pack(side='right', fill='y')
        
        # Start update loop
        self.running = True
        self._update_info()
        
        # Start the tkinter main loop
        self.root.mainloop()
    
    def _update_info(self):
        """Update the information displayed in the window"""
        if not self.running or not self.root:
            return
        
        try:
            # Update basic info
            self.labels['money'].config(text=f"Money: ${self.game_window.game_state.money:.2f}")
            if hasattr(self.game_window, 'market'):
                day_num = self.game_window.market.current_day
                day_name = self.game_window.market.get_day_of_week()
                self.labels['day'].config(text=f"Day {day_num} - {day_name}")
            else:
                self.labels['day'].config(text="Day N/A")
            
            # Update prestige
            prestige = getattr(self.game_window.game_state, 'prestige', 1)
            self.labels['prestige'].config(text=f"Prestige: {prestige}")
            
            # Update barn storage (scan all barn tiles)
            if hasattr(self, 'barn_text'):
                self.barn_text.delete(1.0, tk.END)
                
                # Collect storage from all barn tiles
                barn_contents = {}
                total_barns = 0
                total_capacity = 0
                
                for tile in self.game_window.farm_tiles:
                    if (hasattr(tile, 'state') and tile.state == TILE_BARN and 
                        hasattr(tile, 'stored_crop_type') and tile.stored_crop_type and
                        hasattr(tile, 'stored_amount') and tile.stored_amount > 0):
                        
                        crop_type = tile.stored_crop_type
                        amount = tile.stored_amount
                        
                        if crop_type in barn_contents:
                            barn_contents[crop_type] += amount
                        else:
                            barn_contents[crop_type] = amount
                            
                    # Count total barn capacity
                    if hasattr(tile, 'state') and tile.state == TILE_BARN:
                        total_barns += 1
                        if hasattr(tile, 'building_capacity'):
                            total_capacity += tile.building_capacity
                
                # Display barn contents
                if barn_contents:
                    for crop, amount in barn_contents.items():
                        # Show current market price for each crop  
                        if hasattr(self.game_window, 'market'):
                            market_price = self.game_window.market.get_price(crop)
                            total_value = market_price * amount
                            self.barn_text.insert(tk.END, f"{crop}: {amount} (${market_price:.2f} each = ${total_value:.2f})\n")
                        else:
                            self.barn_text.insert(tk.END, f"{crop}: {amount}\n")
                    
                    # Show summary
                    total_stored = sum(barn_contents.values())
                    self.barn_text.insert(tk.END, f"\nTotal: {total_stored}/{total_capacity} across {total_barns} barn(s)")
                else:
                    if total_barns > 0:
                        self.barn_text.insert(tk.END, f"Empty barns: {total_barns} barn(s) with {total_capacity} total capacity")
                    else:
                        self.barn_text.insert(tk.END, "No barns built")
            
            # Update seed inventory (includes both personal inventory and seed bins)
            if hasattr(self, 'seeds_text'):
                try:
                    self.seeds_text.delete(1.0, tk.END)
                    
                    # Collect seeds from personal inventory
                    total_seeds = {}
                    if self.game_window.game_state.seed_inventory:
                        for seed, amount in self.game_window.game_state.seed_inventory.items():
                            if amount > 0:  # Only show seeds with positive amounts
                                total_seeds[seed] = {'personal': amount, 'bins': 0}
                    
                    # Collect seeds from seed bins
                    if hasattr(self.game_window, 'farm_tiles'):
                        for tile in self.game_window.farm_tiles:
                            if (hasattr(tile, 'state') and tile.state == TILE_SEED_BIN and
                                hasattr(tile, 'stored_crop_type') and tile.stored_crop_type and
                                hasattr(tile, 'stored_amount') and tile.stored_amount > 0):
                                seed_type = tile.stored_crop_type
                                if seed_type not in total_seeds:
                                    total_seeds[seed_type] = {'personal': 0, 'bins': 0}
                                total_seeds[seed_type]['bins'] += tile.stored_amount
                    
                    # Display combined seed inventory
                    if total_seeds:
                        for seed, amounts in total_seeds.items():
                            personal = amounts['personal']
                            bins = amounts['bins']
                            total = personal + bins
                            
                            if bins > 0 and personal > 0:
                                self.seeds_text.insert(tk.END, f"{seed}: {total} ({personal} personal + {bins} in bins)\n")
                            elif bins > 0:
                                self.seeds_text.insert(tk.END, f"{seed}: {bins} (in bins)\n")
                            else:
                                self.seeds_text.insert(tk.END, f"{seed}: {personal} (personal)\n")
                    else:
                        self.seeds_text.insert(tk.END, "No seeds available")
                except Exception as e:
                    print(f"Error in seed inventory update: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Update tractor queue
            if hasattr(self.game_window, 'tractor_job_queue') and hasattr(self, 'queue_text'):
                try:
                    queue_size = len(self.game_window.tractor_job_queue)
                    
                    # Count running tractors
                    running_tractors = 0
                    total_tractors = 0
                    if hasattr(self.game_window, 'managers') and hasattr(self.game_window.managers, 'tractor_manager'):
                        total_tractors = len(self.game_window.managers.tractor_manager.tractors)
                        for tractor in self.game_window.managers.tractor_manager.tractors:
                            if not tractor.is_idle():
                                running_tractors += 1
                    
                    # Calculate idle tractors
                    idle_tractors = total_tractors - running_tractors
                    
                    # Update the queue count label to show running, queued, and idle
                    queue_text = f"Running: {running_tractors} | Queue: {queue_size} | Idle: {idle_tractors}"
                    color = 'orange' if (queue_size > 0 or running_tractors > 0) else 'gray'
                    self.labels['queue_count'].config(text=queue_text, fg=color)
                    
                    self.queue_text.delete(1.0, tk.END)
                    
                    # Show running tractors first
                    if running_tractors > 0:
                        self.queue_text.insert(tk.END, f"🚜 RUNNING TRACTORS ({running_tractors})\n", "header")
                        
                        tractor_count = 0
                        for i, tractor in enumerate(self.game_window.managers.tractor_manager.tractors):
                            if not tractor.is_idle():
                                tractor_count += 1
                                # Get tractor details
                                mode = getattr(tractor, 'mode', 'unknown').title()
                                pos_x = int(tractor.sprite.x // 50) if hasattr(tractor, 'sprite') else 0
                                pos_y = int(tractor.sprite.y // 50) if hasattr(tractor, 'sprite') else 0
                                
                                tractor_desc = f"  T{i+1}: {mode} at ({pos_x}, {pos_y})"
                                
                                # Add additional info if available
                                if hasattr(tractor, 'selected_seed') and tractor.selected_seed:
                                    tractor_desc += f" - {tractor.selected_seed}"
                                elif hasattr(tractor, 'selected_fertilizer') and tractor.selected_fertilizer:
                                    fertilizer_name = tractor.selected_fertilizer.get('name', 'Unknown') if isinstance(tractor.selected_fertilizer, dict) else str(tractor.selected_fertilizer)
                                    tractor_desc += f" - {fertilizer_name}"
                                
                                self.queue_text.insert(tk.END, tractor_desc + "\n")
                        
                        if queue_size > 0:
                            self.queue_text.insert(tk.END, "\n")  # Separator
                    
                    # Show queued jobs
                    if queue_size > 0:
                        self.queue_text.insert(tk.END, f"📋 QUEUED JOBS ({queue_size})\n", "header")
                        
                        # Safely get job queue items - convert deque to list for slicing
                        job_queue = getattr(self.game_window.tractor_job_queue, 'job_queue', [])
                        display_jobs = list(job_queue)[:12]  # Show fewer jobs to make room for running tractors
                        
                        for i, job in enumerate(display_jobs):
                            job_desc = f"  {i+1}. {job.job_type.value.title()} at ({job.grid_x//50}, {job.grid_y//50})"
                            if hasattr(job, 'kwargs') and job.kwargs:
                                if 'num_rows' in job.kwargs:
                                    job_desc += f" ({job.kwargs['num_rows']} rows)"
                                if 'fertilizer_data' in job.kwargs:
                                    fertilizer_name = job.kwargs['fertilizer_data'].get('name', 'Unknown')
                                    job_desc += f" - {fertilizer_name}"
                                if 'seed_type' in job.kwargs:
                                    job_desc += f" - {job.kwargs['seed_type']}"
                            self.queue_text.insert(tk.END, job_desc + "\n")
                        
                        if queue_size > 12:
                            self.queue_text.insert(tk.END, f"  ... and {queue_size - 12} more jobs")
                    
                    # If no running tractors or queued jobs
                    if running_tractors == 0 and queue_size == 0:
                        self.queue_text.insert(tk.END, "No tractors running or jobs queued")
                except Exception as e:
                    print(f"Error in tractor queue update: {e}")
                    import traceback
                    traceback.print_exc()
            elif hasattr(self, 'queue_text'):
                self.labels['queue_count'].config(text="Queue: N/A", fg='gray')
                self.queue_text.delete(1.0, tk.END)
                self.queue_text.insert(tk.END, "Queue system not available")
        
        except Exception as e:
            print(f"Error updating Farm Info window: {e}")  # Debug info
        
        # Schedule next update
        if self.running and self.root:
            self.root.after(100, self._update_info)  # Update every 100ms
    
    def _on_close(self):
        """Handle window close event"""
        self.running = False
        
        try:
            if self.root:
                self.root.quit()
                self.root.destroy()
                self.root = None
        except Exception as e:
            pass  # Can't properly close
            
        self.running = False


# Alias for compatibility
FarmInfoWindow = UIInfoWindow

