#!/usr/bin/env python3
"""
Test script to verify the load game file dialog functionality
"""
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

def test_file_dialog():
    """Test the file dialog for loading save files"""
    # Get the save directory
    save_dir = Path.home() / 'Documents' / 'My Games' / 'A Tile Farming Game'

    # Create a hidden tkinter root for the dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select Save File to Load",
        initialdir=str(save_dir),
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )

    if file_path:
        print(f"Selected file: {file_path}")
        return True
    else:
        print("No file selected (user cancelled)")
        return False

if __name__ == "__main__":
    print("Testing file dialog...")
    test_file_dialog()

