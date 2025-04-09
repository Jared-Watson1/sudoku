import json
import os

SAVE_FILE = "save.txt"


def save_game(current_board, solution_board, givens, notes, difficulty, time_elapsed):
    """Save the current puzzle state to a file."""
    data = {
        "current": current_board,
        "notes": notes,
        "solution": solution_board,
        "givens": givens,
        "difficulty": difficulty,
        "time_elapsed": time_elapsed,
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)


def load_game():
    """Load puzzle state from file, or return None if not found/invalid."""
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r") as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError:
            return None


def clear_save():
    """Delete the save file."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
