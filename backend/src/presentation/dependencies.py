from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.session import get_session
from infrastructure.db.repositories.games_repo import GamesRepository
from infrastructure.db.repositories.leaderboard_repo import (
    LeaderboardRepository
)
from application.services.games_service import GamesService
from application.services.leaderboard_service import LeaderboardService


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


def get_games_service(session: AsyncSession) -> GamesService:
    return GamesService(
        GamesRepository(session),
        LeaderboardRepository(session),
    )


def get_leaderboard_service(session: AsyncSession) -> LeaderboardService:
    games_repo = GamesRepository(session)
    return LeaderboardService(LeaderboardRepository(session), games_repo)
