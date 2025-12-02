from uuid import UUID

from application.errors import NotFound
from domain.game.value_objects import Difficulty
from infrastructure.db.repositories.leaderboard_repo import (
    LeaderboardRepository,
)
from infrastructure.db.repositories.games_repo import GamesRepository


class LeaderboardService:
    def __init__(
        self,
        repo: LeaderboardRepository,
        games_repo: GamesRepository,
    ):
        self.repo = repo
        self.games_repo = games_repo

    async def submit(
        self,
        game_id: UUID,
        duration_seconds: int,
        score: int,
        difficulty: Difficulty,
        player: str | None,
    ):
        game = await self.games_repo.get(game_id)
        if not game:
            raise NotFound("Game not found")
        return await self.repo.add_entry(
            game_id=game_id,
            duration_seconds=duration_seconds,
            score=score,
            difficulty=difficulty,
            player=player,
        )

    async def top10(self):
        return await self.repo.top_entries(10)
