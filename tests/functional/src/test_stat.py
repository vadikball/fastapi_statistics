from http import HTTPStatus

import pytest
from tests.functional.testdata.postgres_data import generate_data

service_url = '/stats'


@pytest.mark.parametrize(
    'body, response',
    [
        (
                {'success': True},
                {'status': HTTPStatus.OK}
        ),
        (
                {'success': False},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        )
    ]
)
@pytest.mark.asyncio
async def test_stat(
        get_data,
        make_request,
        get_params,
        body: dict,
        response: dict
):
    data: list[dict] = get_data()

    if body['success']:
        for stat in data:
            body, headers, status = await make_request('get', service_url, body=stat)
            assert status == response['status']
    else:
        body, headers, status = await make_request('get', service_url, body=body)
        assert status == response['status']

    params = get_params(data)
    body, headers, status = await make_request('get', service_url, query_data=params)

    assert status == HTTPStatus.OK
    body_values = tuple(value for item in body['items'] for value in tuple(item.values()))
    assert data[0]['id'] in body_values

    body, headers, status = await make_request('delete', service_url)

    assert status == HTTPStatus.OK

    params = get_params(data)
    body, headers, status = await make_request('get', service_url, query_data=params)

    assert status == HTTPStatus.NOT_FOUND



# @pytest.mark.asyncio
# async def test_stat_get(
#         get_data,
#         make_request,
#         get_params):
#     data: list[dict] = get_data()
#
#     params = get_params(data)
#     body, headers, status = await make_request('get', service_url, query_data=params)
#
#     assert status == HTTPStatus.OK
#     body_values = tuple(value for item in body['items'] for value in tuple(item.values()))
#     assert data[0]['id'] in body_values
#
#
# @pytest.mark.asyncio
# async def test_stat_delete(
#         get_data,
#         make_request,
#         get_params):
#     data: list[dict] = get_data()
#
#     body, headers, status = await make_request('delete', service_url)
#
#     assert status == HTTPStatus.OK
#
#     params = get_params(data)
#     body, headers, status = await make_request('get', service_url, query_data=params)
#
#     assert status == HTTPStatus.NOT_FOUND
