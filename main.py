import pygame
import sys
from board import (
    Board,
    generate_full_board,
    remove_numbers,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BOARD_OFFSET_X,
    BOARD_OFFSET_Y,
    CELL_SIZE,
    BOARD_SIZE,
)
from save import save_game, load_game, clear_save
from animation import check_number_animation, draw_animation_event, ANIM_DURATION

pygame.init()

# Fonts
FONT_SMALL = pygame.font.SysFont("sans", 18)
FONT_MENU = pygame.font.SysFont("sans", 40)
FONT_TITLE = pygame.font.SysFont("sans", 50)

# Colors
COLOR_BG = (240, 240, 240)
COLOR_HEADER = (50, 100, 150)
COLOR_HEADER_TEXT = (255, 255, 255)


class NumberButton:
    def __init__(self, number, rect):
        self.number = number
        self.rect = rect
        self.visible = True

    def draw(self, win):
        if not self.visible:
            return
        # Draw a background for the button (light gray) and a border.
        pygame.draw.rect(win, (200, 200, 200), self.rect)
        pygame.draw.rect(win, (50, 50, 50), self.rect, 2)
        # Render the button's number.
        text_surf = FONT_SMALL.render(str(self.number), True, (50, 50, 50))
        win.blit(
            text_surf,
            (
                self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                self.rect.y + (self.rect.height - text_surf.get_height()) // 2,
            ),
        )


def draw_top_bar(win, timer_str):
    """Draw a top header with the game title and timer."""
    pygame.draw.rect(win, COLOR_HEADER, (0, 0, WINDOW_WIDTH, 80))
    title_surf = FONT_TITLE.render("SUDŌKU", True, COLOR_HEADER_TEXT)
    win.blit(
        title_surf,
        (
            WINDOW_WIDTH // 2 - title_surf.get_width() // 2,
            40 - title_surf.get_height() // 2,
        ),
    )
    # Timer on the right
    timer_surf = FONT_SMALL.render(timer_str, True, COLOR_HEADER_TEXT)
    win.blit(timer_surf, (WINDOW_WIDTH - 70, 30))


def redraw_window(win, board, note_mode, message, animations, timer_str):
    """Draw everything: background, top bar, board, animations, etc."""
    win.fill(COLOR_BG)

    # Draw top bar with the timer
    draw_top_bar(win, timer_str)

    # Draw note mode info and optional message
    mode_text = "Note Mode: ON" if note_mode else "Note Mode: OFF"
    mode_surf = FONT_SMALL.render(mode_text, True, (255, 255, 255))
    win.blit(mode_surf, (20, 30))

    if message:
        msg_surf = FONT_SMALL.render(message, True, (255, 80, 80))
        win.blit(msg_surf, (20, 55))

    # Draw the board
    board.draw(win)

    # Draw any active animations
    if animations:
        current_time = pygame.time.get_ticks()
        animations[:] = [
            anim for anim in animations if draw_animation_event(win, anim, current_time)
        ]

    pygame.display.update()


def difficulty_menu(win):
    clock = pygame.time.Clock()
    running = True
    chosen = None
    while running:
        win.fill(COLOR_BG)
        pygame.draw.rect(win, COLOR_HEADER, (0, 0, WINDOW_WIDTH, 80))
        title = FONT_MENU.render("Select Difficulty", True, COLOR_HEADER_TEXT)
        win.blit(
            title,
            (WINDOW_WIDTH // 2 - title.get_width() // 2, 40 - title.get_height() // 2),
        )

        # "Buttons"
        easy_text = FONT_MENU.render("Easy", True, (50, 50, 50))
        medium_text = FONT_MENU.render("Medium", True, (50, 50, 50))
        hard_text = FONT_MENU.render("Hard", True, (50, 50, 50))

        easy_rect = easy_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        medium_rect = medium_text.get_rect(center=(WINDOW_WIDTH // 2, 270))
        hard_rect = hard_text.get_rect(center=(WINDOW_WIDTH // 2, 340))

        win.blit(easy_text, easy_rect)
        win.blit(medium_text, medium_rect)
        win.blit(hard_text, hard_rect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if easy_rect.collidepoint(pos):
                    chosen = "easy"
                    running = False
                elif medium_rect.collidepoint(pos):
                    chosen = "medium"
                    running = False
                elif hard_rect.collidepoint(pos):
                    chosen = "hard"
                    running = False
        clock.tick(30)
    return chosen


def main_menu():
    """Basic main menu: new game or resume game."""
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sudoku Main Menu")

    clock = pygame.time.Clock()
    resume_exists = load_game() is not None
    running = True
    game_mode = None
    selected_difficulty = None

    while running:
        win.fill(COLOR_BG)
        pygame.draw.rect(win, COLOR_HEADER, (0, 0, WINDOW_WIDTH, 80))
        title = FONT_TITLE.render("Sudoku", True, COLOR_HEADER_TEXT)
        win.blit(
            title,
            (WINDOW_WIDTH // 2 - title.get_width() // 2, 40 - title.get_height() // 2),
        )

        new_game_text = FONT_MENU.render("New Game", True, (50, 50, 50))
        new_game_rect = new_game_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        win.blit(new_game_text, new_game_rect)

        if resume_exists:
            resume_text = FONT_MENU.render("Resume Game", True, (50, 50, 50))
            resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, 300))
            win.blit(resume_text, resume_rect)
        else:
            resume_rect = None

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if new_game_rect.collidepoint(pos):
                    selected_difficulty = difficulty_menu(win)
                    game_mode = "new"
                    running = False
                elif resume_exists and resume_rect and resume_rect.collidepoint(pos):
                    game_mode = "resume"
                    running = False
        clock.tick(30)

    return game_mode, selected_difficulty


def game_loop(board, difficulty, initial_time=0):
    """
    The main game loop.
    :param board: Board instance
    :param difficulty: "easy", "medium", or "hard"
    :param initial_time: time elapsed from a previous session
    """
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sedoku Game")

    note_mode = False
    clock = pygame.time.Clock()
    message = ""
    animations = []

    # Track row/col/box animations
    solved_rows_animated = set()
    solved_cols_animated = set()
    solved_boxes_animated = set()
    # Track digit animations
    animated_numbers = set()

    # Timer
    time_elapsed = initial_time
    start_ticks = pygame.time.get_ticks()  # in ms

    running = True
    while running:
        # Compute total time (saved + new session)
        current_ticks = pygame.time.get_ticks()
        session_seconds = (current_ticks - start_ticks) // 1000
        total_time = time_elapsed + session_seconds
        # Format as MM:SS
        minutes = total_time // 60
        seconds = total_time % 60
        timer_str = f"{minutes:02d}:{seconds:02d}"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save on quit
                final_time = (
                    time_elapsed + (pygame.time.get_ticks() - start_ticks) // 1000
                )
                c, n, g = board.get_state()
                save_game(c, board.solution, g, n, difficulty, final_time)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.click(pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    note_mode = not note_mode
                elif board.selected and event.unicode in "123456789":
                    row, col = board.selected
                    try:
                        val = int(event.unicode)
                        board.set_cell_value(row, col, val, note_mode)
                    except ValueError:
                        pass
                    # Save progress after each valid move
                    updated_time = (
                        time_elapsed + (pygame.time.get_ticks() - start_ticks) // 1000
                    )
                    c, n, g = board.get_state()
                    save_game(c, board.solution, g, n, difficulty, updated_time)

        # Check row/col/box completions for animations
        current_time = pygame.time.get_ticks()
        for i in range(9):
            if i not in solved_rows_animated:
                # if row i is fully correct
                if all(
                    board.cells[i][j].value != 0
                    and board.cells[i][j].value == board.solution[i][j]
                    for j in range(9)
                ):
                    animations.append(
                        {
                            "type": "row",
                            "index": i,
                            "start_time": current_time,
                            "duration": ANIM_DURATION,
                            "x": (
                                board.BOARD_OFFSET_X
                                if hasattr(board, "BOARD_OFFSET_X")
                                else (
                                    board.offset_x if hasattr(board, "offset_x") else 0
                                )
                            ),
                            # but we'll just use global offsets:
                            "x": 0 + (BOARD_OFFSET_X),
                            "y": BOARD_OFFSET_Y + i * CELL_SIZE,
                            "width": BOARD_SIZE,
                            "height": CELL_SIZE,
                        }
                    )
                    solved_rows_animated.add(i)

        for j in range(9):
            if j not in solved_cols_animated:
                # if column j is fully correct
                if all(
                    board.cells[i][j].value != 0
                    and board.cells[i][j].value == board.solution[i][j]
                    for i in range(9)
                ):
                    animations.append(
                        {
                            "type": "col",
                            "index": j,
                            "start_time": current_time,
                            "duration": ANIM_DURATION,
                            "x": BOARD_OFFSET_X + j * CELL_SIZE,
                            "y": BOARD_OFFSET_Y,
                            "width": CELL_SIZE,
                            "height": BOARD_SIZE,
                        }
                    )
                    solved_cols_animated.add(j)

        for box_row in range(3):
            for box_col in range(3):
                if (box_row, box_col) not in solved_boxes_animated:
                    # check if that 3x3 is correct
                    correct_box = True
                    for r in range(box_row * 3, box_row * 3 + 3):
                        for c in range(box_col * 3, box_col * 3 + 3):
                            if (
                                board.cells[r][c].value == 0
                                or board.cells[r][c].value != board.solution[r][c]
                            ):
                                correct_box = False
                                break
                        if not correct_box:
                            break
                    if correct_box:
                        animations.append(
                            {
                                "type": "box",
                                "index": (box_row, box_col),
                                "start_time": current_time,
                                "duration": ANIM_DURATION,
                                "x": BOARD_OFFSET_X + box_col * 3 * CELL_SIZE,
                                "y": BOARD_OFFSET_Y + box_row * 3 * CELL_SIZE,
                                "width": 3 * CELL_SIZE,
                                "height": 3 * CELL_SIZE,
                            }
                        )
                        solved_boxes_animated.add((box_row, box_col))

        # Check for number-based animations
        new_events = check_number_animation(board, animated_numbers, current_time)
        animations.extend(new_events)

        # Check if entire puzzle is solved
        if board.is_solved():
            final_time = time_elapsed + (pygame.time.get_ticks() - start_ticks) // 1000
            redraw_window(
                win,
                board,
                note_mode,
                "Puzzle Solved!",
                animations,
                f"{final_time//60:02d}:{final_time%60:02d}",
            )
            pygame.time.delay(2000)
            clear_save()
            running = False
            continue

        # Draw everything
        redraw_window(win, board, note_mode, message, animations, timer_str)
        clock.tick(30)


def main():
    while True:
        game_mode, difficulty = main_menu()
        if game_mode == "resume":
            data = load_game()
            if data is None:
                # If no valid save, fallback to new easy
                game_mode, difficulty = "new", "easy"
                data = None
            if data is not None:
                # Resume
                board_instance = Board.from_save(data)
                difficulty = data.get("difficulty", "easy")
                time_elapsed = data.get("time_elapsed", 0)
                game_loop(board_instance, difficulty, time_elapsed)
                continue
        # Else new game
        full_board = generate_full_board()
        if difficulty == "easy":
            removals = 30
        elif difficulty == "medium":
            removals = 40
        else:
            removals = 50
        puzzle_board = remove_numbers(full_board, removals)
        board_instance = Board(puzzle_board, full_board)
        # Immediately save (time_elapsed=0)
        c, n, g = board_instance.get_state()
        save_game(c, board_instance.solution, g, n, difficulty, 0)
        game_loop(board_instance, difficulty, 0)


if __name__ == "__main__":
    main()
