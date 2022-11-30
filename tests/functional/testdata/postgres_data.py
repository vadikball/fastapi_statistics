from decimal import Decimal
from datetime import date
from typing import Optional, Generator
from uuid import uuid4


def generate_data(
        views: Optional[int] = None,
        clicks: Optional[int] = None,
        cost: Optional[Decimal] = None
) -> Generator:

    yield {
        'id': uuid4(),
        'date': date.today(),
        'views': views,
        'clicks': clicks,
        'cost': cost
    }


def easy_case() -> list[dict]:
    data = list()
    data.append(generate_data().__next__())
    data.append(generate_data(1000, 100, Decimal(10)).__next__())
    data.append(generate_data(100).__next__())
    return data
