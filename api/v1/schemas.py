from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, condecimal


class StatSchemaIn(BaseModel):
    date: date
    views: Optional[int]
    clicks: Optional[int]
    cost: condecimal(gt=Decimal(0), max_digits=2, decimal_places=2)


class StatSchemaOut(BaseModel):
    date: date
    views: Optional[int]
    clicks: Optional[int]
    cost: Optional[condecimal(gt=Decimal(0), max_digits=5, decimal_places=2)]
    cpc: Optional[condecimal(gt=Decimal(0), max_digits=5, decimal_places=2)]
    cpm: Optional[condecimal(gt=Decimal(0), max_digits=5, decimal_places=2)]
