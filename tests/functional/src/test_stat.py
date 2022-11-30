from http import HTTPStatus

import pytest

service_url = '/stats'


@pytest.mark.asyncio
async def test_stat(
        get_data,
        make_request,
        get_params,
):
    data: list[dict] = get_data()

    for stat in data:
        body, headers, status = await make_request('post', service_url, body=stat)
        assert status == HTTPStatus.OK

    body, headers, status = await make_request('post', service_url, body={'success': False})
    assert status == HTTPStatus.UNPROCESSABLE_ENTITY

    params = get_params(data)
    body, headers, status = await make_request('get', service_url, query_data=params)
    assert status == HTTPStatus.OK

    assert len(body['items']) >= 3

    body, headers, status = await make_request('delete', service_url)
    assert status == HTTPStatus.OK

    params = get_params(data)
    body, headers, status = await make_request('get', service_url, query_data=params)
    assert status == HTTPStatus.NOT_FOUND
