from sqlalchemy.ext.asyncio import AsyncEngine

from models.stat import StatModel


async def create_all(postgres_engine: AsyncEngine):
    async with postgres_engine.begin() as conn:
        await conn.run_sync(StatModel.metadata.create_all)
