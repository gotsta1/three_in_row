from domain.game.match_finder import find_matches
from domain.game.gravity import apply_gravity


def test_find_matches_horizontal():
    board = [
        ["A", "A", "A"],
        ["B", "C", "D"],
        ["E", "F", "G"],
    ]
    matches = find_matches(board)
    assert (0, 0) in matches and (0, 1) in matches and (0, 2) in matches


def test_gravity_drops_and_refills():
    board = [
        ["A", "B"],
        ["A", "B"],
        ["A", "C"],
    ]
    matches = {(0, 0), (1, 0), (2, 0)}
    new_board, removed = apply_gravity(board, matches, items_count=3)
    assert len(removed) == 3
    # column 0 filled with new symbols
    assert new_board[0][0] is not None and new_board[1][0] is not None and new_board[2][0] is not None
