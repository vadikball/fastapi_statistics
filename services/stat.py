from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql import text as sa_text
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models.stat import StatModel
from services.utils import SearchParams


class StatService:

    def __init__(self, session):
        self.session = session

    async def delete_all_data(self):
        """
            Удаляет все записи в таблице
        """
        async with self.session() as session:
            async with session.begin():
                await session.execute(sa_text(""" TRUNCATE TABLE stats CASCADE """))
                await session.commit()

    async def add_stat(self, stat: StatModel) -> dict:
        """
            Добавляет запись в таблицу
        :param stat: Заполненная данными модель таблицы
        :return: dict с информацией о добавленной модели
        """
        async with self.session() as session:
            async with session.begin():
                stat = await session.merge(stat)
                await session.commit()
                stat = stat.dict()
        return stat

    async def list_stat(self, params: SearchParams) -> tuple[dict]:
        """
            Возращает список словарей,
            в которые сериализованы объекты StatModel
        """

        raw_params = params.to_raw_params()
        query = select(StatModel).\
            where(StatModel.date.between(params.start, params.end)).\
            offset(raw_params.offset).\
            limit(raw_params.limit).\
            order_by(getattr(StatModel, params.sort.value))

        async with self.session() as session:
            async with session.begin():
                stats: tuple[StatModel] = tuple((await session.scalars(query)).all())
                stats: tuple[dict] = tuple(stat.dict() for stat in stats)

        return stats


@lru_cache()
def get_stat_service(
        async_session: AsyncSession = Depends(get_session),
) -> StatService:
    return StatService(async_session)
