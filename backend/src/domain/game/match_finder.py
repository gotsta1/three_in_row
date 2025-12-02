from typing import Set, Tuple


Coord = Tuple[int, int]


def find_matches(board: list[list[str]]) -> Set[Coord]:
    rows = len(board)
    cols = len(board[0]) if rows else 0
    matched: Set[Coord] = set()
    for r in range(rows):
        streak = 1
        for c in range(1, cols):
            if board[r][c] == board[r][c - 1]:
                streak += 1
            else:
                if streak >= 3:
                    for k in range(streak):
                        matched.add((r, c - 1 - k))
                streak = 1
        if streak >= 3:
            for k in range(streak):
                matched.add((r, cols - 1 - k))
    for c in range(cols):
        streak = 1
        for r in range(1, rows):
            if board[r][c] == board[r - 1][c]:
                streak += 1
            else:
                if streak >= 3:
                    for k in range(streak):
                        matched.add((r - 1 - k, c))
                streak = 1
        if streak >= 3:
            for k in range(streak):
                matched.add((rows - 1 - k, c))
    return matched
