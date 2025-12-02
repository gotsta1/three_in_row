import random
from typing import List

from domain.game.item_codec import index_to_item
from domain.game.match_finder import find_matches
from domain.game.move_finder import has_possible_move


def available_items(count: int) -> List[str]:
    return [index_to_item(i) for i in range(count)]


def generate_board(rows: int, cols: int, items_count: int) -> list[list[str]]:
    items = available_items(items_count)
    attempts = 0
    while True:
        board: list[list[str]] = [
            [random.choice(items) for _ in range(cols)] for _ in range(rows)
        ]
        for r in range(rows):
            for c in range(cols):
                board[r][c] = _pick_non_matching(board, r, c, items)
        if rows < 3 and cols < 3:
            return board
        if not find_matches(board) and has_possible_move(board):
            return board
        attempts += 1
        if attempts > 5:
            return board


def _pick_non_matching(
    board: list[list[str]],
    r: int,
    c: int,
    items: list[str],
) -> str:
    for _ in range(10):
        candidate = random.choice(items)
        board[r][c] = candidate
        if not _creates_match(board, r, c):
            return candidate
    return board[r][c]


def _creates_match(board: list[list[str]], r: int, c: int) -> bool:
    val = board[r][c]
    rows = len(board)
    cols = len(board[0])
    count = 1
    cc = c - 1
    while cc >= 0 and board[r][cc] == val:
        count += 1
        cc -= 1
    cc = c + 1
    while cc < cols and board[r][cc] == val:
        count += 1
        cc += 1
    if count >= 3:
        return True
    count = 1
    rr = r - 1
    while rr >= 0 and board[rr][c] == val:
        count += 1
        rr -= 1
    rr = r + 1
    while rr < rows and board[rr][c] == val:
        count += 1
        rr += 1
    return count >= 3
