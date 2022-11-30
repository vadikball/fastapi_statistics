from http import HTTPStatus

import pytest
from tests.functional.testdata.postgres_data import generate_data

service_url = '/stats'


@pytest.mark.parametrize(
    'body, response',
    [
        (
                generate_data().__next__(),
                {'status': HTTPStatus.OK}
        ),
        (
                {'success': False},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        )
    ]
)
@pytest.mark.asyncio
async def test_stat_post(
        make_request,
        body: dict,
        response: dict
):
    body, headers, status = make_request('get', service_url, body=body)

    assert status == response['status']


@pytest.mark.asyncio
async def test_stat_get(
        get_data,
        make_request):
    data: list[dict] = get_data()

    body, headers, status = make_request('get', service_url)

    assert status == HTTPStatus.OK
    body_values = tuple(*tuple(item.values()) for item in body['items'])
    assert data[0]['id'] in body_values


@pytest.mark.asyncio
async def test_stat_delete(
        make_request):

    body, headers, status = make_request('delete', service_url)

    assert status == HTTPStatus.OK

    body, headers, status = make_request('get', service_url)

    assert status == HTTPStatus.NOT_FOUND
