from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from domain.game.value_objects import Difficulty, Direction


class CustomConfigDTO(BaseModel):
    rows: int = Field(ge=3)
    cols: int = Field(ge=3)
    target_score: int = Field(gt=0)
    items_count: int = Field(default=6, gt=1, le=100)
    one_swap_reset: bool = False
    random_item_mode: bool = False
    timeout_seconds: int = Field(default=3600, gt=0)
    random_item: Optional[str] = None


class CreateGameRequest(BaseModel):
    difficulty: Difficulty = Difficulty.easy
    custom: Optional[CustomConfigDTO] = None
    player: str = Field(min_length=1)


class GameResponse(BaseModel):
    id: UUID
    board: List[List[str]]
    score: int
    status: str
    target_score: int
    difficulty: Difficulty
    random_item: Optional[str] = None
    player: str


class SwapRequest(BaseModel):
    row: int
    col: int
    direction: Direction


class SnapshotResponse(BaseModel):
    board: List[List[str]]
    score: int
    status: str
    reset_applied: bool = False


class ResetResponse(BaseModel):
    board: List[List[str]]
    score: int
    status: str
    reset_applied: bool = True
