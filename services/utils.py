from enum import Enum
from typing import Optional

from fastapi import Query
from fastapi_pagination import Params
from pydantic.typing import Literal


class SortChoice(Enum):
    date = 'date'
    views = 'views'
    clicks = 'clicks'
    cost = 'cost'


class SortParams(Params):
    sort: Optional[SortChoice] = Query(default='date')


class SearchParams(SortParams):
    start: str = Query(default=...)
    end: str = Query(default=...)
