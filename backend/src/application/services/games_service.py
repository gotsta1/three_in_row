import datetime as dt
from uuid import UUID

from domain.game import engine
from domain.game.config_presets import preset_for_difficulty
from domain.game.entities import Snapshot
from domain.game.rules import ensure_active
from domain.game.value_objects import Difficulty, Move
from infrastructure.db.repositories.games_repo import GamesRepository
from infrastructure.db.repositories.leaderboard_repo import (
    LeaderboardRepository,
)
from application.errors import NotFound


def _ensure_aware(value: dt.datetime) -> dt.datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=dt.timezone.utc)
    return value


class GamesService:
    def __init__(
        self,
        repo: GamesRepository,
        leaderboard_repo: LeaderboardRepository | None = None,
    ):
        self.repo = repo
        self.leaderboard_repo = leaderboard_repo

    async def create_game(
        self,
        difficulty: Difficulty,
        custom,
        player: str,
    ) -> UUID:
        player_name = player.strip()
        if not player_name:
            raise ValueError("Player name required")
        if difficulty == Difficulty.custom:
            if not custom:
                raise ValueError(
                    "Custom config required for custom difficulty"
                )
            config = custom
        else:
            config = preset_for_difficulty(difficulty)
        game = await self.repo.create_game(
            difficulty=difficulty,
            rows=config.rows,
            cols=config.cols,
            target_score=config.target_score,
            items_count=config.items_count,
            one_swap_reset=config.one_swap_reset,
            random_item_mode=config.random_item_mode,
            timeout_seconds=config.timeout_seconds,
            random_item=getattr(config, "random_item", None),
            player=player_name,
        )
        return game.id

    async def get_game(self, game_id: UUID):
        game = await self.repo.get(game_id)
        if not game:
            raise NotFound("Game not found")
        return game

    async def make_move(
        self,
        game_id: UUID,
        move: Move,
        now: dt.datetime | None = None,
    ) -> list[Snapshot]:
        game = await self.get_game(game_id)
        timestamp = now or dt.datetime.now(dt.timezone.utc)
        ensure_active(game, timestamp)
        snapshots = engine.apply_swap(game, move, timestamp)
        await self.repo.save(game)
        if game.status == "won" and self.leaderboard_repo:
            duration_seconds = int(
                (
                    _ensure_aware(timestamp)
                    - _ensure_aware(game.created_at)
                ).total_seconds()
            )
            already = await self.leaderboard_repo.has_entry_for_game(game.id)
            if not already:
                await self.leaderboard_repo.add_entry(
                    game_id=game.id,
                    duration_seconds=duration_seconds,
                    score=game.score,
                    difficulty=game.difficulty,
                    player=game.player,
                )
        return snapshots

    async def reset_board(
        self,
        game_id: UUID,
        now: dt.datetime | None = None,
    ) -> Snapshot:
        game = await self.get_game(game_id)
        snapshot = engine.apply_reset(
            game,
            now or dt.datetime.now(dt.timezone.utc),
        )
        await self.repo.save(game)
        return snapshot
