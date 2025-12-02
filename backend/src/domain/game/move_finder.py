from domain.game.match_finder import find_matches


def has_possible_move(board: list[list[str]]) -> bool:
    """Возвращает True, если рядом есть свап, дающий совпадение."""
    rows = len(board)
    cols = len(board[0]) if rows else 0
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols:
                if _swap_creates_match(board, r, c, r, c + 1):
                    return True
            if r + 1 < rows:
                if _swap_creates_match(board, r, c, r + 1, c):
                    return True
    return False


def _swap_creates_match(
    board: list[list[str]],
    r1: int,
    c1: int,
    r2: int,
    c2: int,
) -> bool:
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
    has_match = bool(find_matches(board))
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
    return has_match
