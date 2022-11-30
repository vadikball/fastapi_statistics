from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql import text as sa_text
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models.stat import StatModel
from services.utils import SearchParams


class StatService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete_all_data(self):
        async with self.session.begin():
            await self.session.execute(sa_text(""" TRUNCATE TABLE stats CASCADE """))

    async def add_stat(self, stat: StatModel):
        async with self.session.begin():
            stat = await self.session.merge(stat)

        return stat

    async def get_search(self, params: SearchParams) -> tuple[StatModel]:
        """

        """

        raw_params = params.to_raw_params()
        query = select(StatModel).\
            where(StatModel.date.between(params.start, params.end)).\
            offset(raw_params.offset).\
            limit(raw_params.limit).\
            order_by(getattr(StatModel, params.sort.value))

        stats: tuple[StatModel] = tuple(await self.session.execute(query))

        return stats


@lru_cache()
def get_stat_service(
        async_session: AsyncSession = Depends(get_session),
) -> StatService:
    return StatService(async_session)
