from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.settings import settings
from presentation.exception_handlers import setup_exception_handlers
from presentation.routers import games, leaderboard, health


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description="Match-3 backend with stateless persistence",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(games.router)
    app.include_router(leaderboard.router)
    setup_exception_handlers(app)
    return app


app = create_app()
