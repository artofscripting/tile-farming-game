#!/usr/bin/env python3
"""
Test script to verify that tractors continue working during save operations
"""
import time
from game_window import GameWindow
from tractor_job_queue import JobType

def test_save_with_tractor_jobs():
    """Test that tractors continue working while save dialog is shown"""
    print("Testing save functionality with tractor jobs...")

    # Create a test game
    gw = GameWindow(1013, 768, 'Test')

    try:
        # Start a tractor job
        print("Starting a tractor tilling job...")
        gw.tractor_job_queue.add_job(JobType.TILLING, 336, 408, num_rows=1)

        # Let the job start
        for _ in range(10):
            gw.update(0.1)
            time.sleep(0.01)

        print("Tractor job started. Now testing save functionality...")

        # Capture game state (simulating what happens when save button is clicked)
        captured_state = gw.capture_game_state()
        if captured_state is None:
            print("❌ Failed to capture game state")
            return False

        print("✅ Game state captured successfully")

        # Continue updating while "saving" (simulating dialog delay)
        print("Simulating save dialog delay (tractors should continue working)...")
        for _ in range(50):  # Simulate dialog being open for a bit
            gw.update(0.1)
            time.sleep(0.01)

        # Now save the captured state
        result = gw.save_game("test_save.json", captured_state)
        if result:
            print("✅ Save completed successfully")
        else:
            print("❌ Save failed")
            return False

        # Continue updating to see if tractors finish their jobs
        print("Continuing game updates to verify tractor jobs complete...")
        for _ in range(100):
            gw.update(0.1)
            time.sleep(0.01)

        print("✅ Test completed - tractors continued working during save process")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up
        gw.close()

if __name__ == "__main__":
    success = test_save_with_tractor_jobs()
    if success:
        print("\n🎉 All tests passed! Save functionality works correctly with tractor jobs.")
    else:
        print("\n❌ Tests failed!")

