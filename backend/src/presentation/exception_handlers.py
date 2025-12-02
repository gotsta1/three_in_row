from fastapi import Request
from fastapi.responses import JSONResponse

from application.errors import NotFound
from domain.game.errors import InvalidMove, GameExpired, GameFinished


def setup_exception_handlers(app):
    @app.exception_handler(NotFound)
    async def not_found_handler(request: Request, exc: NotFound):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InvalidMove)
    async def invalid_move_handler(request: Request, exc: InvalidMove):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(GameExpired)
    async def expired_handler(request: Request, exc: GameExpired):
        return JSONResponse(
            status_code=410,
            content={"detail": "Game expired"},
        )

    @app.exception_handler(GameFinished)
    async def finished_handler(request: Request, exc: GameFinished):
        return JSONResponse(
            status_code=400,
            content={"detail": f"Game already {exc.status}"},
        )
