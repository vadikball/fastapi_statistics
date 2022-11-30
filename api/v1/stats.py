from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, create_page
from fastapi_pagination.bases import AbstractPage

from api.v1.schemas import (StatSchemaIn,
                            StatSchemaOut)
from services.stat import (get_stat_service,
                           StatService,
                           StatModel,
                           SearchParams)

router = APIRouter(tags=['Статистика'])


@router.get(
    '/',
    response_model=Page[StatSchemaOut],
    summary="Просмотр статистики",
    description="Список записей статистики",
    response_description="id, имя, описание"
)
async def stat_list(
        params: SearchParams = Depends(),
        stat_service: StatService = Depends(get_stat_service)
) -> AbstractPage[StatSchemaOut]:
    """ Статистика списком """

    stats = await stat_service.get_search(
        params
    )
    if not stats:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='stats not found'
        )

    total = len(stats)

    stats = [StatSchemaOut(**stat.dict()) for stat in stats]
    return create_page(stats, total, params)


@router.post(
    '/',
    response_model=StatSchemaOut,
    summary="Добавление статистики",
    description="Добавление статистики",
    response_description="id, название, описание"
)
async def add_stat(
        stat: StatSchemaIn,
        stat_service: StatService = Depends(get_stat_service)
) -> StatSchemaOut:
    """ Добавление статистики """

    stat: StatModel = await stat_service.add_stat(StatModel(**stat.dict()))
    if not stat.id:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail='Unprocessable Entity')

    return StatSchemaOut(**stat.dict())


@router.delete(
    '/',
    response_model=dict[str, str],
    summary="Удалить статистику",
    description="Удаление всех записей статистики",
    response_description="описание"
)
async def truncate_stat(
        stat_service: StatService = Depends(get_stat_service)
) -> dict[str, str]:
    """ Удаление статистики """

    await stat_service.delete_all_data()

    return {'detail': 'ok'}
