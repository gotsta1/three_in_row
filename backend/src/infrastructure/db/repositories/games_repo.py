import datetime as dt
import random
from typing import Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from domain.game.board_gen import generate_board, available_items
from domain.game.entities import GameState
from domain.game.value_objects import Difficulty
from infrastructure.db.models.game import GameModel


class GamesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_game(
        self,
        difficulty: Difficulty,
        rows: int,
        cols: int,
        target_score: int,
        items_count: int,
        one_swap_reset: bool,
        random_item_mode: bool,
        timeout_seconds: int,
        random_item: Optional[str] = None,
        player: str = "player",
    ) -> GameState:
        board = generate_board(rows, cols, items_count)
        random_choice = random_item or (
            random.choice(available_items(items_count))
            if random_item_mode
            else None
        )
        model = GameModel(
            board=board,
            rows=rows,
            cols=cols,
            score=0,
            target_score=target_score,
            difficulty=difficulty.value,
            status="active",
            one_swap_reset=one_swap_reset,
            random_item_mode=random_item_mode,
            random_item=random_choice,
            items_count=items_count,
            timeout_seconds=timeout_seconds,
            player=player,
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.commit()
        return self._to_state(model)

    async def get(self, game_id: UUID) -> Optional[GameState]:
        result = await self.session.execute(
            select(GameModel).where(GameModel.id == game_id)
        )
        model = result.scalar_one_or_none()
        return self._to_state(model) if model else None

    async def save(self, game: GameState) -> None:
        await self.session.execute(
            update(GameModel)
            .where(GameModel.id == game.id)
            .values(
                board=game.board,
                score=game.score,
                status=game.status,
                last_move_at=game.last_move_at,
                updated_at=dt.datetime.now(dt.timezone.utc),
            )
        )
        await self.session.commit()

    @staticmethod
    def _to_state(model: GameModel) -> GameState:
        return GameState(
            id=model.id,
            created_at=model.created_at,
            board=model.board,
            rows=model.rows,
            cols=model.cols,
            score=model.score,
            target_score=model.target_score,
            difficulty=Difficulty(model.difficulty),
            status=model.status,
            last_move_at=model.last_move_at,
            one_swap_reset=model.one_swap_reset,
            random_item_mode=model.random_item_mode,
            random_item=model.random_item,
            items_count=model.items_count,
            timeout_seconds=model.timeout_seconds,
            player=model.player,
        )
