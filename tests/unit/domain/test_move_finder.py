from domain.game.move_finder import has_possible_move


def test_has_possible_move_true():
    board = [
        ["A", "B", "A"],
        ["B", "A", "A"],
        ["C", "D", "E"],
    ]
    assert has_possible_move(board) is True  # swap (0,1) with (1,1) makes triple A


def test_has_possible_move_false():
    board = [
        ["A", "B", "C"],
        ["D", "E", "F"],
        ["G", "H", "I"],
    ]
    assert has_possible_move(board) is False
