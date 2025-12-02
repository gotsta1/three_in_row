from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from domain.game.value_objects import Difficulty


class LeaderboardEntryDTO(BaseModel):
    id: UUID
    game_id: UUID
    difficulty: Difficulty
    duration_seconds: int
    score: int
    player: Optional[str] = None


class SubmitResultRequest(BaseModel):
    game_id: UUID
    duration_seconds: int = Field(gt=0)
    player: Optional[str] = None
    difficulty: Difficulty
    score: int


class LeaderboardResponse(BaseModel):
    entries: List[LeaderboardEntryDTO]
