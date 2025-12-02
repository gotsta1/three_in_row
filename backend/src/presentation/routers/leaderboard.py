from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.dto.leaderboard import (
    LeaderboardResponse,
    LeaderboardEntryDTO,
    SubmitResultRequest,
)
from application.services.leaderboard_service import LeaderboardService
from presentation.dependencies import get_db_session, get_leaderboard_service

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("", response_model=LeaderboardResponse)
async def top(session: AsyncSession = Depends(get_db_session)):
    service: LeaderboardService = get_leaderboard_service(session)
    entries = await service.top10()
    dto = [
        LeaderboardEntryDTO(
            id=e.id,
            game_id=e.game_id,
            difficulty=e.difficulty,
            duration_seconds=e.duration_seconds,
            score=e.score,
            player=e.player,
        )
        for e in entries
    ]
    return LeaderboardResponse(entries=dto)


@router.post("", response_model=LeaderboardEntryDTO)
async def submit(
    payload: SubmitResultRequest,
    session: AsyncSession = Depends(get_db_session),
):
    service: LeaderboardService = get_leaderboard_service(session)
    entry = await service.submit(
        game_id=payload.game_id,
        duration_seconds=payload.duration_seconds,
        score=payload.score,
        difficulty=payload.difficulty,
        player=payload.player,
    )
    return LeaderboardEntryDTO(
        id=entry.id,
        game_id=entry.game_id,
        difficulty=entry.difficulty,
        duration_seconds=entry.duration_seconds,
        score=entry.score,
        player=entry.player,
    )
