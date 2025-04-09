# Sudoku

Sudoku is a Sudoku puzzle game built with Python and [pygame](https://www.pygame.org/). The app provides an intuitive interface that supports both keyboard entry and mouse interactions for cell input. It includes visual enhancements such as cell, row, and column highlighting, as well as highlighting of cells with matching values. Additionally, number buttons on the right side of the board let users enter values by clicking. When all valid occurrences of a number have been filled, the corresponding button disappears.

## File Overview

### main.py
- **Purpose:**  
  Serves as the entry point for the game. Handles window setup, main menu, difficulty selection, and the main game loop.
- **Key Features:**  
  - **Menus:** Main and difficulty menus for selecting game mode (new or resume) and difficulty level.
  - **Game Loop:** Processes keyboard and mouse inputs, updates game state, manages animations, and saves progress.
  - **Number Buttons:** Implements a side-panel of clickable buttons (numbers 1–9). When a button’s number is fully placed correctly on the board (checked against the solution), that button is hidden.

### board.py
- **Purpose:**  
  Contains the core logic for the Sudoku board and cell management.
- **Key Features:**  
  - **Cell Class:** Represents each Sudoku cell with properties for value, notes, if it’s a given (preset), and error indication.
  - **Board Class:**  
    - Manages an array of `Cell` instances and handles drawing the grid.
    - Draws highlights for the selected cell’s row, column, and same-value cells.
    - Generates a complete Sudoku puzzle (`generate_full_board`) and creates a playable puzzle by removing numbers (`remove_numbers`).
    - **New Addition:** The `is_number_complete(num)` method checks whether all occurrences of a specific number have been correctly filled in according to the solution.

### animation.py
- **Purpose:**  
  Manages visual animations that celebrate completed rows, columns, boxes, or full occurrences of a number.
- **Key Features:**  
  - **Animations:** Uses a fading overlay effect for highlighting completed sections.
  - **Constants:** Defines animation duration (`ANIM_DURATION`) and colors for the overlay effects.
  - **Functions:**  
    - `draw_animation_event(win, event, current_time)`: Draws a fading overlay.
    - `check_number_animation(...)`: Checks if a number appears in each 3x3 box and triggers animations.

### save.py
- **Purpose:**  
  Handles saving and loading game state to/from a file.
- **Key Features:**  
  - **save_game:** Saves the current board state, solution, notes, given status, difficulty, and elapsed time.
  - **load_game:** Reads the saved state if it exists.
  - **clear_save:** Deletes the save file, used when a puzzle is solved.

## How to Run

1. **Install Dependencies:**  
   Ensure you have Python 3.10+ and pygame installed. You can install pygame via pip:
   ```bash
   pip install pygame
