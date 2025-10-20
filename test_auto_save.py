import os
import time
from game_window import GameWindow

# Test auto-save functionality
print("Testing auto-save functionality...")

# Create game
gw = GameWindow(1013, 768, 'Test')

# Check that autosave.json doesn't exist initially
if os.path.exists('autosave.json'):
    os.remove('autosave.json')
    print("Removed existing autosave.json")

print("Starting game - auto-save should trigger in 2 minutes...")

# Run the game for 125 seconds (a bit more than 2 minutes) to ensure auto-save triggers
start_time = time.time()
while time.time() - start_time < 125:
    # Process pyglet events (this is needed for the scheduled updates to run)
    import pyglet
    pyglet.clock.tick()
    gw.update(1/60.0)  # Simulate one frame
    time.sleep(0.01)  # Small delay to not hog CPU

# Check if autosave.json was created
if os.path.exists('autosave.json'):
    print("✅ Auto-save successful! autosave.json was created")
    
    # Check file size to make sure it's not empty
    file_size = os.path.getsize('autosave.json')
    print(f"Auto-save file size: {file_size} bytes")
    
    if file_size > 1000:  # Should be at least 1KB for a valid save
        print("✅ Auto-save file appears to contain valid data")
    else:
        print("❌ Auto-save file seems too small")
        
else:
    print("❌ Auto-save failed! autosave.json was not created")

# Clean up
gw.close()
if os.path.exists('autosave.json'):
    os.remove('autosave.json')
    print("Cleaned up autosave.json")

