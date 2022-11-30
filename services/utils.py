from datetime import date
from enum import Enum
from typing import Optional

from fastapi import Query
from fastapi_pagination import Params
import orjson
from pydantic.typing import Literal


def orjson_dumps(v, *, default):
    """ orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем """

    return orjson.dumps(v, default=default).decode()


class SortChoice(Enum):
    date = 'date'
    views = 'views'
    clicks = 'clicks'
    cost = 'cost'


class SortParams(Params):
    sort: Optional[SortChoice] = Query(default='date')

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class SearchParams(SortParams):
    start: date = Query(default=...)
    end: date = Query(default=...)
