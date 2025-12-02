import copy
import datetime as dt
from typing import List

from domain.game.board_gen import generate_board, available_items
from domain.game.entities import GameState, Snapshot
from domain.game.errors import InvalidMove
from domain.game.gravity import apply_gravity
from domain.game.match_finder import find_matches
from domain.game.move_finder import has_possible_move
from domain.game.rules import ensure_active
from domain.game.scoring import compute_score, apply_reset_penalty
from domain.game.value_objects import Move, Direction


def apply_swap(
    game: GameState,
    move: Move,
    now: dt.datetime,
) -> List[Snapshot]:
    ensure_active(game, now)
    board = copy.deepcopy(game.board)
    dr, dc = _direction_delta(move.direction)
    r2 = move.row + dr
    c2 = move.col + dc
    if not _in_bounds(move.row, move.col, game) or not _in_bounds(
        r2,
        c2,
        game,
    ):
        raise InvalidMove("Out of bounds")
    board[move.row][move.col], board[r2][c2] = (
        board[r2][c2],
        board[move.row][move.col],
    )

    matches = find_matches(board)
    if not matches:
        if game.one_swap_reset:
            return [apply_reset(game, now, triggered_by_swap=True)]
        raise InvalidMove("Swap produced no match")

    score = game.score
    status = game.status
    snapshots: List[Snapshot] = []
    while matches:
        board, removed = apply_gravity(board, matches, game.items_count)
        gained = compute_score(
            removed,
            game.random_item_mode,
            game.random_item,
        )
        score += gained
        if score >= game.target_score:
            status = "won"
        snapshots.append(
            Snapshot(board=copy.deepcopy(board), score=score, status=status)
        )
        if status == "won":
            break
        matches = find_matches(board)

    if status == "active" and not has_possible_move(board):
        board = generate_board(game.rows, game.cols, game.items_count)
        snapshots.append(
            Snapshot(
                board=copy.deepcopy(board),
                score=score,
                status=status,
                reset_applied=True,
            )
        )

    game.board = board
    game.score = score
    game.status = status
    game.last_move_at = now
    return snapshots


def apply_reset(
    game: GameState,
    now: dt.datetime,
    triggered_by_swap: bool = False,
) -> Snapshot:
    ensure_active(game, now)
    board = generate_board(game.rows, game.cols, game.items_count)
    new_score = apply_reset_penalty(game.score)
    game.board = board
    game.score = new_score
    game.last_move_at = now
    return Snapshot(
        board=board,
        score=new_score,
        status=game.status,
        reset_applied=True,
    )


def _direction_delta(direction: Direction) -> tuple[int, int]:
    if direction == Direction.up:
        return -1, 0
    if direction == Direction.down:
        return 1, 0
    if direction == Direction.left:
        return 0, -1
    if direction == Direction.right:
        return 0, 1
    raise InvalidMove("Unknown direction")


def _in_bounds(r: int, c: int, game: GameState) -> bool:
    return 0 <= r < game.rows and 0 <= c < game.cols
