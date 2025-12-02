from typing import List
from uuid import UUID

from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from domain.game.value_objects import Difficulty
from infrastructure.db.models.leaderboard import LeaderboardEntry


class LeaderboardRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_entry(
        self,
        game_id: UUID,
        duration_seconds: int,
        score: int,
        difficulty: Difficulty,
        player: str | None,
    ) -> LeaderboardEntry:
        entry = LeaderboardEntry(
            game_id=game_id,
            duration_seconds=duration_seconds,
            score=score,
            difficulty=difficulty.value,
            player=player,
        )
        self.session.add(entry)
        await self.session.flush()
        await self.session.commit()
        return entry

    async def has_entry_for_game(self, game_id: UUID) -> bool:
        result = await self.session.execute(
            select(LeaderboardEntry.id).where(
                LeaderboardEntry.game_id == game_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def top_entries(
        self,
        limit: int = 10,
    ) -> List[LeaderboardEntry]:
        result = await self.session.execute(
            select(LeaderboardEntry)
            .order_by(asc(LeaderboardEntry.duration_seconds))
            .limit(limit)
        )
        return list(result.scalars().all())
