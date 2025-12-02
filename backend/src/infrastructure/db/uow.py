from contextlib import asynccontextmanager
from typing import Callable, Awaitable

from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self, session_factory: Callable[[], Awaitable[AsyncSession]]):
        self._session_factory = session_factory

    @asynccontextmanager
    async def __call__(self):
        session: AsyncSession = await self._session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
