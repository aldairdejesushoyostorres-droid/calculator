import json
import os

HISTORY_FILE = "calculator_history.json"

def load_history():
    """Loads calculation history from the JSON file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            # Return empty list if file is corrupted or unreadable
            return []
    return []

def save_history(history):
    """Saves the current calculation history to the JSON file."""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)
    except IOError:
        # Handle case where file cannot be written (e.g., permissions issue)
        print("Error: Could not save history file.")

def add_to_history(history, calculation_string, result):
    """Adds a new entry to the history list."""
    entry = f"{calculation_string} = {result}"
    history.append(entry)
    # Limit history size to 100 entries to prevent infinite growth
    if len(history) > 100:
        history.pop(0) 
    return history