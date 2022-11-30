from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, condecimal


class StatSchemaIn(BaseModel):
    date: date
    views: Optional[int] = None
    clicks: Optional[int] = None
    cost: Optional[condecimal(gte=Decimal(0), max_digits=5, decimal_places=2)] = None


class StatSchemaOut(BaseModel):
    date: date
    views: Optional[int] = None
    clicks: Optional[int] = None
    cost: Optional[condecimal(gt=Decimal(0), max_digits=5, decimal_places=2)] = None
    cpc: Optional[condecimal(gt=Decimal(0), max_digits=5, decimal_places=2)] = None
    cpm: Optional[condecimal(gt=Decimal(0), max_digits=5, decimal_places=2)] = None
