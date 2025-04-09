import pygame
from board import BOARD_OFFSET_X, BOARD_OFFSET_Y, CELL_SIZE, BOARD_SIZE

ANIM_DURATION = 1000  # 1 second
ANIM_COLOR = (0, 255, 0)  # bright green overlay


def draw_animation_event(win, event, current_time):
    """Draw a fading overlay if the animation is still active."""
    elapsed = current_time - event["start_time"]
    if elapsed > event["duration"]:
        return False
    alpha = int(255 * (1 - elapsed / event["duration"]))
    overlay = pygame.Surface((event["width"], event["height"]), pygame.SRCALPHA)
    overlay.fill((ANIM_COLOR[0], ANIM_COLOR[1], ANIM_COLOR[2], alpha))
    win.blit(overlay, (event["x"], event["y"]))
    return True


def check_number_animation(board, animated_numbers, current_time):
    """
    If a digit (1..9) appears at least once in *every* 3x3 sub-grid,
    create an animation for each cell containing that digit.
    """
    events = []
    for num in range(1, 10):
        if num in animated_numbers:
            continue
        # Check each 3x3 box for at least one 'num'
        all_boxes = True
        for box_row in range(3):
            for box_col in range(3):
                found = False
                for i in range(box_row * 3, box_row * 3 + 3):
                    for j in range(box_col * 3, box_col * 3 + 3):
                        if board.cells[i][j].value == num:
                            found = True
                            break
                    if found:
                        break
                if not found:
                    all_boxes = False
                    break
            if not all_boxes:
                break

        if all_boxes:
            # Animate every cell that has this number
            for i in range(9):
                for j in range(9):
                    if board.cells[i][j].value == num:
                        x = BOARD_OFFSET_X + j * CELL_SIZE
                        y = BOARD_OFFSET_Y + i * CELL_SIZE
                        events.append(
                            {
                                "type": "number",
                                "number": num,
                                "start_time": current_time,
                                "duration": ANIM_DURATION,
                                "x": x,
                                "y": y,
                                "width": CELL_SIZE,
                                "height": CELL_SIZE,
                            }
                        )
            animated_numbers.add(num)
    return events
