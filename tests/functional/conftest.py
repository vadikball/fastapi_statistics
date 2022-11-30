import asyncio
from typing import Any, Optional

import aiohttp
import pytest
import pytest_asyncio
from multidict import CIMultiDictProxy

from tests.functional.settings import test_settings
from tests.functional.testdata.postgres_data import easy_case


@pytest.fixture(scope='session')
def event_loop():
    """ event_loop для тестовой сессии """

    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def aiohttp_session():
    """ aiohttp клиент для сессии """

    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
async def load_test_data():
    """ генератор тестовых данных """

    data: list[dict] = easy_case()
    yield data
    pass


@pytest.fixture
def get_data(load_test_data: list[dict]):
    """ Доставляет тестовые данные в тело тестовой функции """
    def inner():
        return load_test_data

    return inner


@pytest.fixture
def get_params():
    """ генерирует параметры запросы get """

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
        """

            :param method: 'get', 'post', 'delete'
            :param endpoint: url, по которому запрашиваем данные
            :param query_data: параметры запросы
            :param body: тело запроса
            :return: тело ответа, заголовки, статус ответа
        """

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
