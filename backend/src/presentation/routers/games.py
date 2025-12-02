import datetime as dt
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.dto.games import (
    CreateGameRequest,
    GameResponse,
    SnapshotResponse,
    SwapRequest,
    ResetResponse,
)
from application.services.games_service import GamesService
from domain.game.value_objects import Move
from presentation.dependencies import get_db_session, get_games_service

router = APIRouter(prefix="/games", tags=["games"])


@router.post("", response_model=GameResponse)
async def create_game(
    payload: CreateGameRequest,
    session: AsyncSession = Depends(get_db_session),
):
    service = get_games_service(session)
    game_id = await service.create_game(
        payload.difficulty,
        payload.custom,
        payload.player,
    )
    game = await service.get_game(game_id)
    return GameResponse(
        id=game.id,
        board=game.board,
        score=game.score,
        status=game.status,
        target_score=game.target_score,
        difficulty=game.difficulty,
        random_item=game.random_item,
        player=game.player,
    )


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    service = get_games_service(session)
    game = await service.get_game(game_id)
    return GameResponse(
        id=game.id,
        board=game.board,
        score=game.score,
        status=game.status,
        target_score=game.target_score,
        difficulty=game.difficulty,
        random_item=game.random_item,
        player=game.player,
    )


@router.post("/{game_id}/swap", response_model=list[SnapshotResponse])
async def swap(
    game_id: UUID,
    payload: SwapRequest,
    session: AsyncSession = Depends(get_db_session),
):
    service = get_games_service(session)
    snapshots = await service.make_move(
        game_id,
        Move(row=payload.row, col=payload.col, direction=payload.direction),
        now=dt.datetime.utcnow(),
    )
    return [SnapshotResponse(**s.__dict__) for s in snapshots]


@router.post("/{game_id}/reset", response_model=ResetResponse)
async def reset(
    game_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    service = get_games_service(session)
    snapshot = await service.reset_board(game_id, now=dt.datetime.utcnow())
    return ResetResponse(**snapshot.__dict__)
