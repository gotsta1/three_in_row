import datetime as dt

from domain.game.errors import GameExpired, GameFinished
from domain.game.entities import GameState


def _ensure_aware(value: dt.datetime) -> dt.datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=dt.timezone.utc)
    return value


def ensure_active(game: GameState, now: dt.datetime) -> None:
    if game.status == "won" or game.status == "lost":
        raise GameFinished(game.status)
    now_aware = _ensure_aware(now)
    last_move = _ensure_aware(game.last_move_at)
    if (now_aware - last_move).total_seconds() >= game.timeout_seconds:
        raise GameExpired()
