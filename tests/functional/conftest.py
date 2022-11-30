import asyncio
from typing import Any, Optional

import aiohttp
import pytest
import pytest_asyncio
from multidict import CIMultiDictProxy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text as sa_text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from models.stat import StatModel
import tests.functional.utils.base as pg_base
from tests.functional.settings import test_settings
from tests.functional.testdata.postgres_data import easy_case


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
async def postgres_engine() -> AsyncEngine:
    engine = create_async_engine(
        test_settings.pg_settings,
        future=True,
        echo=True,
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def postgres_session(postgres_engine: AsyncEngine) -> AsyncSession:
    session = sessionmaker(
        postgres_engine, expire_on_commit=False, class_=AsyncSession
    )()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
async def load_test_data(postgres_engine: AsyncEngine,
                         postgres_session: AsyncSession):
    await pg_base.create_all(postgres_engine)
    data: list[dict] = easy_case()

    try:
        for stat in data:
            await postgres_session.merge(StatModel(**stat))
    except:
        await postgres_session.rollback()
    else:
        await postgres_session.commit()

    yield data

    await postgres_session.execute(sa_text('TRUNCATE TABLE stats CASCADE'))
    await postgres_session.commit()


@pytest.fixture
def get_data(load_test_data: list[dict]):
    def inner():
        return load_test_data

    return inner


@pytest.fixture
def get_params():
    def inner(data: list[dict]):
        date = str(data[0]['date'])
        params = {'start': date, 'end': date}

        return params

    return inner


@pytest.fixture
def make_request(aiohttp_session: aiohttp.ClientSession):
    async def inner(
            method: str,
            endpoint: str,
            query_data: Optional[dict] = None,
            body: Optional[dict] = None
    ) -> tuple[Any, CIMultiDictProxy[str], int]:

        url = test_settings.service_url + '/api/v1' + endpoint
        request_params = {
            'method': method,
            'url': url,
        }
        if query_data is not None:
            request_params['params'] = query_data
        if body is not None:
            request_params['json'] = body

        async with aiohttp_session.request(**request_params) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        return body, headers, status

    return inner
