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
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def add_to_history(history, calculation_string, result):
    """Adds a new entry to the history list."""
    entry = f"{calculation_string} = {result}"
    history.append(entry)
    # Ensure history does not grow infinitely large (e.g., limit to 100 entries)
    if len(history) > 100:
        history.pop(0) # Remove the oldest entry
    return history