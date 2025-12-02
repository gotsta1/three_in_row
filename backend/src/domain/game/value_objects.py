from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Direction(str, Enum):
    up = "up"
    down = "down"
    left = "left"
    right = "right"


@dataclass(frozen=True)
class Move:
    row: int
    col: int
    direction: Direction


class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
    custom = "custom"


@dataclass
class CustomConfig:
    rows: int
    cols: int
    target_score: int
    items_count: int = 6
    one_swap_reset: bool = False
    random_item_mode: bool = False
    timeout_seconds: int = 3600
    random_item: Optional[str] = None
