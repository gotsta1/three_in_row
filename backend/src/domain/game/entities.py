import datetime as dt
from dataclasses import dataclass, replace
from typing import List, Optional
from uuid import UUID

from domain.game.value_objects import Difficulty


@dataclass
class GameState:
    id: UUID
    created_at: dt.datetime
    player: str
    board: List[List[str]]
    rows: int
    cols: int
    score: int
    target_score: int
    difficulty: Difficulty
    status: str
    last_move_at: dt.datetime
    one_swap_reset: bool
    random_item_mode: bool
    random_item: Optional[str]
    items_count: int
    timeout_seconds: int

    def with_board(
        self,
        board: List[List[str]],
        score: int,
        status: Optional[str],
        last_move_at: dt.datetime,
    ) -> "GameState":
        return replace(
            self,
            board=board,
            score=score,
            status=status or self.status,
            last_move_at=last_move_at,
        )


@dataclass
class Snapshot:
    board: List[List[str]]
    score: int
    status: str
    reset_applied: bool = False
