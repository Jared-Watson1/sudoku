import pygame
import random

# Window / Board layout constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700

BOARD_SIZE = 540  # 9x9 board -> each cell is 60px if BOARD_SIZE=540
CELL_SIZE = BOARD_SIZE // 9

# Position the board within the window
BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_SIZE) // 2  # horizontally centered
BOARD_OFFSET_Y = 100  # room at top for header

# Colors and Fonts
COLOR_BG = (240, 240, 240)  # main background
COLOR_HEADER = (50, 100, 150)
COLOR_HEADER_TEXT = (255, 255, 255)
COLOR_CELL_BG = (255, 255, 255)
COLOR_CELL_LINES = (160, 185, 220)
COLOR_HIGHLIGHT = (210, 230, 255)  # highlight row/col
COLOR_HIGHLIGHT_SEL = (100, 190, 255)  # highlight selected cell
COLOR_SAME_VALUE = (255, 235, 130, 100)  # RGBA with transparency
COLOR_GIVEN = (30, 30, 30)
COLOR_USER = (40, 80, 220)
COLOR_INCORRECT = (255, 80, 80)

pygame.font.init()
FONT_CELL = pygame.font.SysFont("sans", 32, bold=True)
FONT_NOTE = pygame.font.SysFont("sans", 16)


# Puzzle Generation Functions
def valid(board, row, col, num):
    """Check if placing num at board[row][col] is valid with Sudoku rules."""
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_x = (col // 3) * 3
    box_y = (row // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_y + i][box_x + j] == num:
                return False
    return True


def solve_board(board):
    """Backtracking solver to fill board in-place with a valid solution."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                candidates = list(range(1, 10))
                random.shuffle(candidates)
                for num in candidates:
                    if valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def generate_full_board():
    """Generate a complete 9x9 Sudoku solution."""
    board = [[0] * 9 for _ in range(9)]
    solve_board(board)
    return board


def remove_numbers(board, removals=40):
    """Create a puzzle by removing 'removals' cells from a full board."""
    puzzle = [row[:] for row in board]
    count = removals
    while count > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            count -= 1
    return puzzle


# --------------------------------------------------------------------------------
# Cell and Board Classes
# --------------------------------------------------------------------------------
class Cell:
    def __init__(self, value, row, col, given):
        self.value = value
        self.row = row
        self.col = col
        self.given = given
        self.notes = []
        self.incorrect = False

    def draw(self, win):
        """Draw the cell (value or notes)."""
        x = BOARD_OFFSET_X + self.col * CELL_SIZE
        y = BOARD_OFFSET_Y + self.row * CELL_SIZE

        # Fill background
        pygame.draw.rect(win, COLOR_CELL_BG, (x, y, CELL_SIZE, CELL_SIZE))

        # If there's a value, draw it
        if self.value != 0:
            text_color = COLOR_GIVEN if self.given else COLOR_USER
            if self.incorrect:
                text_color = COLOR_INCORRECT
            val_surf = FONT_CELL.render(str(self.value), True, text_color)
            win.blit(
                val_surf,
                (
                    x + (CELL_SIZE - val_surf.get_width()) // 2,
                    y + (CELL_SIZE - val_surf.get_height()) // 2,
                ),
            )
        # Otherwise, draw candidate notes
        elif self.notes:
            sorted_notes = sorted(self.notes)
            sub_size = CELL_SIZE / 2
            for i, note in enumerate(sorted_notes):
                sub_x = x + (i % 2) * sub_size
                sub_y = y + (i // 2) * sub_size
                note_surf = FONT_NOTE.render(str(note), True, (80, 80, 80))
                note_x = sub_x + (sub_size - note_surf.get_width()) / 2
                note_y = sub_y + (sub_size - note_surf.get_height()) / 2
                win.blit(note_surf, (note_x, note_y))


class Board:
    def __init__(self, puzzle, solution):
        """
        puzzle: 9x9 with some zeros (the puzzle).
        solution: the fully solved board.
        """
        self.cells = [[None] * 9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                given = puzzle[i][j] != 0
                self.cells[i][j] = Cell(puzzle[i][j], i, j, given)
        self.solution = solution
        self.selected = None

    def draw(self, win):
        """Draw the board including semi-transparent highlights for the selected cell,
        its row, column, and all same-value cells."""
        # Draw every cell normally first
        for row in self.cells:
            for cell in row:
                cell.draw(win)

        # If a cell is selected, apply overlays
        if self.selected:
            sel_row, sel_col = self.selected

            # Create semi-transparent overlay surfaces.
            # Adjust the alpha value (fourth value in RGBA) as needed.
            highlight_overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            highlight_overlay.fill(
                (210, 230, 255, 100)
            )  # Light blue for row & column (alpha=100)

            selected_overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            selected_overlay.fill(
                (100, 190, 255, 150)
            )  # Stronger blue for the selected cell (alpha=150)

            # Draw the row highlight.
            for col in range(9):
                hx = BOARD_OFFSET_X + col * CELL_SIZE
                hy = BOARD_OFFSET_Y + sel_row * CELL_SIZE
                win.blit(highlight_overlay, (hx, hy))

            # Draw the column highlight.
            for row in range(9):
                hx = BOARD_OFFSET_X + sel_col * CELL_SIZE
                hy = BOARD_OFFSET_Y + row * CELL_SIZE
                win.blit(highlight_overlay, (hx, hy))

            # Draw the overlay for the selected cell.
            sx = BOARD_OFFSET_X + sel_col * CELL_SIZE
            sy = BOARD_OFFSET_Y + sel_row * CELL_SIZE
            win.blit(selected_overlay, (sx, sy))

            # Highlight other cells that share the same value as the selected cell.
            selected_value = self.cells[sel_row][sel_col].value
            if selected_value != 0:
                same_val_overlay = pygame.Surface(
                    (CELL_SIZE, CELL_SIZE), pygame.SRCALPHA
                )
                same_val_overlay.fill(
                    (255, 235, 130, 100)
                )  # Semi-transparent yellowish overlay (alpha=100)
                for r in range(9):
                    for c in range(9):
                        if (r, c) != (sel_row, sel_col) and self.cells[r][
                            c
                        ].value == selected_value:
                            overlay_x = BOARD_OFFSET_X + c * CELL_SIZE
                            overlay_y = BOARD_OFFSET_Y + r * CELL_SIZE
                            win.blit(same_val_overlay, (overlay_x, overlay_y))

        # Draw grid lines on top so board structure remains clear.
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1

            # Horizontal grid lines
            start_x = BOARD_OFFSET_X
            start_y = BOARD_OFFSET_Y + i * CELL_SIZE
            end_x = BOARD_OFFSET_X + BOARD_SIZE
            pygame.draw.line(
                win, COLOR_CELL_LINES, (start_x, start_y), (end_x, start_y), line_width
            )

            # Vertical grid lines
            start_x = BOARD_OFFSET_X + i * CELL_SIZE
            start_y = BOARD_OFFSET_Y
            end_y = BOARD_OFFSET_Y + BOARD_SIZE
            pygame.draw.line(
                win, COLOR_CELL_LINES, (start_x, start_y), (start_x, end_y), line_width
            )

    def click(self, pos):
        """Set self.selected if the click is on the board."""
        x, y = pos
        if (
            BOARD_OFFSET_X <= x < BOARD_OFFSET_X + BOARD_SIZE
            and BOARD_OFFSET_Y <= y < BOARD_OFFSET_Y + BOARD_SIZE
        ):
            col = (x - BOARD_OFFSET_X) // CELL_SIZE
            row = (y - BOARD_OFFSET_Y) // CELL_SIZE
            self.selected = (row, col)
            return (row, col)
        return None

    def set_cell_value(self, row, col, value, note_mode=False):
        """Set a cell's value or toggle notes. Mark incorrect if it doesn't match solution."""
        cell = self.cells[row][col]
        if cell.given:
            return
        if note_mode:
            if value in cell.notes:
                cell.notes.remove(value)
            elif len(cell.notes) < 4:
                cell.notes.append(value)
        else:
            cell.value = value
            cell.notes = []
            cell.incorrect = self.solution[row][col] != value

    def is_solved(self):
        """Check if all cells match the solution."""
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                if cell.value == 0 or cell.value != self.solution[i][j]:
                    return False
        return True

    def get_state(self):
        """Return the puzzle data for saving."""
        current = [[cell.value for cell in row] for row in self.cells]
        notes = [[cell.notes for cell in row] for row in self.cells]
        givens = [[1 if cell.given else 0 for cell in row] for row in self.cells]
        return current, notes, givens

    def is_number_complete(self, num):
        """Return True if every cell that should contain num (per the solution) has num filled in."""
        return all(
            self.cells[i][j].value == num
            for i in range(9)
            for j in range(9)
            if self.solution[i][j] == num
        )

    @classmethod
    def from_save(cls, data):
        """Reconstruct a Board from saved JSON data."""
        current = data["current"]
        solution = data["solution"]
        givens_data = data["givens"]
        notes_data = data["notes"]

        instance = cls.__new__(cls)
        instance.cells = [[None] * 9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                given = givens_data[i][j] == 1
                c = Cell(current[i][j], i, j, given)
                c.notes = notes_data[i][j] if notes_data[i][j] else []
                instance.cells[i][j] = c
        instance.solution = solution
        instance.selected = None
        return instance
