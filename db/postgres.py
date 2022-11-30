from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from db.base import Base
from core.config import settings

engine: Optional[AsyncEngine] = None
session: Optional[AsyncSession] = None


class AsyncDatabaseSession:
    def __init__(self):
        self._session = session
        self._engine = engine

    def __getattr__(self, name):
        return getattr(self._session, name)

    # def init(self):
    #     self._engine = create_async_engine(
    #         settings.DB_CONFIG,
    #         future=True,
    #         echo=True,
    #     )
    #     self._session = sessionmaker(
    #         self._engine, expire_on_commit=False, class_=AsyncSession
    #     )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        await self._session.close()
        await self._engine.dispose()


db: Optional[AsyncDatabaseSession] = None


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    return session
