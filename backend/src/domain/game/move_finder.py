from domain.game.match_finder import find_matches


def has_possible_move(board: list[list[str]]) -> bool:
    """Возвращает True, если рядом есть свап, дающий совпадение."""
    rows = len(board)
    cols = len(board[0]) if rows else 0
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols and _would_match(board, r, c, r, c + 1):
                return True
            if r + 1 < rows and _would_match(board, r, c, r + 1, c):
                return True
    return False


def _would_match(
    board: list[list[str]],
    r1: int,
    c1: int,
    r2: int,
    c2: int,
) -> bool:
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
    try:
        return _cell_in_match(board, r1, c1) or _cell_in_match(board, r2, c2)
    finally:
        board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]


def _cell_in_match(board: list[list[str]], r: int, c: int) -> bool:
    val = board[r][c]
    if val is None:
        return False
    rows = len(board)
    cols = len(board[0]) if rows else 0

    left = c
    while left - 1 >= 0 and board[r][left - 1] == val:
        left -= 1
    right = c
    while right + 1 < cols and board[r][right + 1] == val:
        right += 1
    if right - left + 1 >= 3:
        return True

    up = r
    while up - 1 >= 0 and board[up - 1][c] == val:
        up -= 1
    down = r
    while down + 1 < rows and board[down + 1][c] == val:
        down += 1
    return down - up + 1 >= 3
