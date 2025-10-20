import json
import time
from game_window import GameWindow
from tractor_job_queue import JobType

# Create game and set up tractors with jobs
gw = GameWindow(1013, 768, 'Test')

# Set up some tractor jobs
print("=== Setting up tractor jobs ===")
gw.tractor_job_queue.add_job(JobType.TILLING, 1, 1, num_rows=3)
gw.tractor_job_queue.add_job(JobType.PLANTING, 2, 2, seed_type='Carrot', num_rows=1)
gw.tractor_job_queue.add_job(JobType.HARVESTING, 3, 3, num_rows=2)

print(f"Jobs in queue: {len(gw.tractor_job_queue)}")
print(f"Queue status: {gw.tractor_job_queue.get_queue_status()}")

# Modify tractor states
tractor = gw.tractors[0]
tractor.x = 100
tractor.y = 200
tractor.core.mode = 1  # Set to some mode
tractor.core.selected_seed = 'Carrot'

print("\n=== Before Save ===")
print(f"Tractor 0 position: ({tractor.x}, {tractor.y})")
print(f"Tractor 0 mode: {tractor.core.mode}")
print(f"Tractor 0 selected seed: {tractor.core.selected_seed}")
print(f"Jobs in queue: {len(gw.tractor_job_queue)}")

# Save game
result = gw.save_game('test_tractor_jobs.json')
print(f"\nSave result: {result}")

# Check what's saved
with open('test_tractor_jobs.json', 'r') as f:
    data = json.load(f)
    if 'tractors' in data and data['tractors']:
        tractor_data = data['tractors'][0]
        print("\n=== Saved Tractor Data ===")
        print(f"Tractor x: {tractor_data.get('x')}")
        print(f"Tractor y: {tractor_data.get('y')}")
        print(f"Tractor mode: {tractor_data.get('mode')}")
        print(f"Tractor selected_seed: {tractor_data.get('selected_seed')}")
    
    if 'tractor_job_queue' in data:
        print(f"\n=== Saved Job Queue Data ===")
        print(f"Number of jobs: {len(data['tractor_job_queue'])}")
        for i, job_data in enumerate(data['tractor_job_queue']):
            print(f"Job {i}: {job_data['job_type']} at ({job_data['grid_x']}, {job_data['grid_y']}) - {job_data.get('kwargs', {})}")

# Create new game and load
print("\n=== Loading Game ===")
gw2 = GameWindow(1013, 768, 'Test2')
result = gw2.load_game('test_tractor_jobs.json')
print(f"Load result: {result}")

# Check loaded tractor
loaded_tractor = gw2.tractors[0]
print("\n=== After Load ===")
print(f"Tractor 0 position: ({loaded_tractor.x}, {loaded_tractor.y})")
print(f"Tractor 0 mode: {loaded_tractor.core.mode}")
print(f"Tractor 0 selected seed: {loaded_tractor.core.selected_seed}")
print(f"Jobs in queue: {len(gw2.tractor_job_queue)}")
print(f"Queue status: {gw2.tractor_job_queue.get_queue_status()}")

# Check individual jobs
if gw2.tractor_job_queue.job_queue:
    for i, job in enumerate(gw2.tractor_job_queue.job_queue):
        print(f"Job {i}: {job.job_type.value} at ({job.grid_x}, {job.grid_y}) - {job.kwargs}")

gw.close()
gw2.close()

