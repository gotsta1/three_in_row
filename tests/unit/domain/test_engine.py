import datetime as dt

from domain.game import engine
from domain.game.entities import GameState
from domain.game.value_objects import Difficulty, Move, Direction


def _game_state(board, **kwargs) -> GameState:
    rows = len(board)
    cols = len(board[0])
    now = dt.datetime.now(dt.timezone.utc)
    return GameState(
        id=kwargs.get("id", None),
        created_at=now,
        board=board,
        rows=rows,
        cols=cols,
        score=kwargs.get("score", 0),
        target_score=kwargs.get("target_score", 50),
        difficulty=kwargs.get("difficulty", Difficulty.easy),
        status=kwargs.get("status", "active"),
        last_move_at=now,
        one_swap_reset=kwargs.get("one_swap_reset", False),
        random_item_mode=kwargs.get("random_item_mode", False),
        random_item=kwargs.get("random_item", None),
        items_count=kwargs.get("items_count", 6),
        timeout_seconds=kwargs.get("timeout_seconds", 3600),
        player=kwargs.get("player", "test"),
    )


def test_swap_with_matches_adds_score():
    # Swapping (0,1) down creates two horizontal triples (row0: AAA, row1: BBB)
    board = [
        ["A", "B", "A"],
        ["B", "A", "B"],
        ["C", "C", "A"],
    ]
    game = _game_state(board, items_count=3, target_score=10)
    snaps = engine.apply_swap(game, Move(row=0, col=1, direction=Direction.down), game.created_at + dt.timedelta(seconds=1))
    assert game.score >= 6  # base match removes 6; cascades may add more
    assert snaps, "Snapshots should be returned when matches occur"
    assert snaps[0].score >= 6


def test_random_item_scoring_counts_only_target_item():
    board = [
        ["A", "B", "A"],
        ["B", "A", "B"],
        ["C", "C", "A"],
    ]
    game = _game_state(board, items_count=3, random_item_mode=True, random_item="A", target_score=10)
    snaps = engine.apply_swap(game, Move(row=0, col=1, direction=Direction.down), game.created_at + dt.timedelta(seconds=1))
    assert game.score == 3  # only three As removed
    assert snaps and snaps[0].score == 3


def test_one_swap_reset_triggers_when_no_match():
    board = [
        ["A", "B", "C"],
        ["D", "E", "F"],
        ["G", "H", "I"],
    ]
    game = _game_state(board, items_count=9, one_swap_reset=True, score=10)
    snaps = engine.apply_swap(game, Move(row=0, col=0, direction=Direction.right), game.created_at + dt.timedelta(seconds=1))
    assert len(snaps) == 1
    assert snaps[0].reset_applied is True
    assert game.score == 5  # penalty applied
    assert game.status == "active"
