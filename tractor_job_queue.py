"""
Tractor Job Queue System - Manages queued tractor operations
"""
from enum import Enum
from collections import deque
import time
from constants import TILE_OWNED, TILE_TILLED, TILE_READY_HARVEST, TILE_SEED_BIN, TILE_GROWING


class JobType(Enum):
    """Types of tractor jobs that can be queued"""
    TILLING = "tilling"
    PLANTING = "planting"
    HARVESTING = "harvesting"
    FERTILIZING = "fertilizing"
    CULTIVATOR = "cultivator"


class TractorJob:
    """Represents a single tractor job to be executed"""
    
    def __init__(self, job_type, grid_x, grid_y, game_window, **kwargs):
        self.job_type = job_type
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.game_window = game_window
        self.kwargs = kwargs  # Additional parameters specific to job type
        self.timestamp = time.time()  # When the job was created
        
    def execute(self, tractor):
        """Execute this job with the given tractor"""
        try:
            if self.job_type == JobType.TILLING:
                num_rows = self.kwargs.get('num_rows', 1)
                return tractor.start_tilling_multi_row(
                    self.grid_y, self.game_window.width, self.game_window, 
                    self.grid_x, num_rows
                )
                
            elif self.job_type == JobType.PLANTING:
                seed_type = self.kwargs.get('seed_type')
                num_rows = self.kwargs.get('num_rows', 1)
                return tractor.start_planting_multi_row(
                    self.grid_y, self.game_window.width, self.game_window, 
                    self.grid_x, seed_type, num_rows
                )
                
            elif self.job_type == JobType.HARVESTING:
                num_rows = self.kwargs.get('num_rows', 1)
                return tractor.start_harvesting_multi_row(
                    self.grid_y, self.game_window.width, self.game_window, 
                    self.grid_x, num_rows
                )
                
            elif self.job_type == JobType.FERTILIZING:
                fertilizer_data = self.kwargs.get('fertilizer_data')
                num_rows = self.kwargs.get('num_rows', 1)
                return tractor.start_cultivating_multi_row(
                    self.grid_y, self.game_window.width, self.game_window, 
                    self.grid_x, fertilizer_data, num_rows
                )
                
            elif self.job_type == JobType.CULTIVATOR:
                num_rows = self.kwargs.get('num_rows', 1)
                return tractor.start_cultivator_multi_row(
                    self.grid_y, self.game_window.width, self.game_window, 
                    self.grid_x, num_rows
                )
                
        except Exception as e:
            print(f"Error executing tractor job {self.job_type}: {e}")
            return False
            
        return False
    
    def __str__(self):
        return f"TractorJob({self.job_type.value} at {self.grid_x},{self.grid_y})"


class TractorJobQueue:
    """Manages a queue of tractor jobs and executes them when tractors become available"""
    
    def __init__(self, game_window):
        self.game_window = game_window
        self.job_queue = deque()
        self.max_queue_size = 20  # Prevent infinite queue growth
        
    def add_job(self, job_type, grid_x, grid_y, **kwargs):
        """Add a new job to the queue"""
        if len(self.job_queue) >= self.max_queue_size:
            print(f"Tractor job queue is full! Cannot queue {job_type.value} job.")
            return False
            
        job = TractorJob(job_type, grid_x, grid_y, self.game_window, **kwargs)
        self.job_queue.append(job)
        print(f"Queued {job_type.value} job at position ({grid_x},{grid_y}) - {len(self.job_queue)} jobs in queue")
        return True
    
    def process_queue(self):
        """Check for available tractors and execute queued jobs"""
        if not self.job_queue:
            return
            
        # Try to execute jobs while we have available tractors and queued jobs
        while self.job_queue:
            available_tractor = self.game_window.get_available_tractor()
            if not available_tractor:
                break  # No available tractors, wait for later
                
            job = self.job_queue.popleft()
            
            # Validate that the job is still valid (tiles might have changed)
            if self._is_job_valid(job):
                success = job.execute(available_tractor)
                if success:
                    print(f"Executed queued {job.job_type.value} job - {len(self.job_queue)} jobs remaining")
                else:
                    print(f"Failed to execute queued {job.job_type.value} job (conditions changed)")
            else:
                print(f"Skipped invalid queued {job.job_type.value} job (tile conditions changed)")
    
    def _is_job_valid(self, job):
        """Check if a queued job is still valid to execute"""
        tile = self.game_window.get_tile_at_position(job.grid_x, job.grid_y)
        if not tile:
            return False
            
        # Basic validation based on job type
        if job.job_type == JobType.TILLING:
            return tile.state == TILE_OWNED
        elif job.job_type == JobType.PLANTING:
            seed_type = job.kwargs.get('seed_type')
            if not seed_type:
                return False
            # Check if tile is tilled
            if tile.state != TILE_TILLED:
                return False
            # Check if seeds are available in seed bins
            has_seeds = False
            for bin_tile in self.game_window.farm_tiles:
                if (bin_tile.state == TILE_SEED_BIN and 
                    bin_tile.stored_crop_type == seed_type and 
                    bin_tile.stored_amount > 0):
                    has_seeds = True
                    break
            return has_seeds
        elif job.job_type == JobType.HARVESTING:
            return tile.state == TILE_READY_HARVEST
        elif job.job_type == JobType.FERTILIZING:
            return tile.state in [TILE_TILLED, TILE_GROWING, TILE_READY_HARVEST]
        elif job.job_type == JobType.CULTIVATOR:
            return True  # Cultivator can work on most farmed tiles
            
        return False
    
    def clear_queue(self):
        """Clear all queued jobs"""
        count = len(self.job_queue)
        self.job_queue.clear()
        if count > 0:
            print(f"Cleared {count} queued tractor jobs")
    
    def get_queue_status(self):
        """Get information about the current queue"""
        if not self.job_queue:
            return "No jobs queued"
            
        job_types = {}
        for job in self.job_queue:
            job_type = job.job_type.value
            job_types[job_type] = job_types.get(job_type, 0) + 1
            
        status_parts = []
        for job_type, count in job_types.items():
            status_parts.append(f"{count} {job_type}")
            
        return f"Queued: {', '.join(status_parts)} ({len(self.job_queue)} total)"
    
    def get_queued_positions(self):
        """Return a list of (grid_x, grid_y) positions with queued jobs"""
        positions = []
        for job in self.job_queue:
            positions.append((job.grid_x, job.grid_y))
        return positions
    
    def cancel_job_at_position(self, grid_x, grid_y):
        """Cancel the first job found at the specified position"""
        for i, job in enumerate(self.job_queue):
            if job.grid_x == grid_x and job.grid_y == grid_y:
                cancelled_job = self.job_queue[i]
                del self.job_queue[i]
                print(f"Cancelled {cancelled_job.job_type.value} job at position ({grid_x},{grid_y}) - {len(self.job_queue)} jobs remaining")
                return True
        return False
    
    def __len__(self):
        """Return the number of jobs in the queue"""
        return len(self.job_queue)
    
    def save_job_data(self):
        """Save the current job queue state"""
        jobs_data = []
        for job in self.job_queue:
            job_data = {
                'job_type': job.job_type.value,
                'grid_x': job.grid_x,
                'grid_y': job.grid_y,
                'kwargs': job.kwargs.copy(),
                'timestamp': job.timestamp
            }
            jobs_data.append(job_data)
        return jobs_data
    
    def load_job_data(self, jobs_data):
        """Load job queue state from saved data"""
        self.job_queue.clear()
        for job_data in jobs_data:
            try:
                job_type = JobType(job_data['job_type'])
                grid_x = job_data['grid_x']
                grid_y = job_data['grid_y']
                kwargs = job_data.get('kwargs', {})
                timestamp = job_data.get('timestamp', time.time())
                
                job = TractorJob(job_type, grid_x, grid_y, self.game_window, **kwargs)
                job.timestamp = timestamp
                self.job_queue.append(job)
            except Exception as e:
                print(f"Error loading tractor job: {e}")
                continue
        
        if self.job_queue:
            print(f"Loaded {len(self.job_queue)} tractor jobs from save file")

