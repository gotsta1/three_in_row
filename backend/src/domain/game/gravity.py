import random
from typing import Tuple

from domain.game.board_gen import available_items


def apply_gravity(
    board: list[list[str]],
    matches: set[tuple[int, int]],
    items_count: int,
) -> Tuple[list[list[str]], list[str]]:
    rows = len(board)
    cols = len(board[0]) if rows else 0
    removed_items: list[str] = []
    for r, c in matches:
        removed_items.append(board[r][c])
        board[r][c] = None
    for c in range(cols):
        write_row = rows - 1
        for read_row in range(rows - 1, -1, -1):
            if board[read_row][c] is not None:
                board[write_row][c] = board[read_row][c]
                write_row -= 1
        for fill_row in range(write_row, -1, -1):
            board[fill_row][c] = random.choice(available_items(items_count))
    return board, removed_items
