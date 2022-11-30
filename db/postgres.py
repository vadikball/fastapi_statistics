from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from db.base import Base

engine: Optional[AsyncEngine] = None
session: Optional[AsyncSession] = None


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    return session
