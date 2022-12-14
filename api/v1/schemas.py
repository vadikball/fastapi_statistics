from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, condecimal


class StatSchemaIn(BaseModel):
    date: date
    views: Optional[int] = None
    clicks: Optional[int] = None
    cost: Optional[condecimal(ge=Decimal(0), max_digits=5, decimal_places=2)] = None


class StatSchemaOut(StatSchemaIn):
    cpc: Optional[condecimal(gt=Decimal(0), max_digits=5, decimal_places=2)] = None
    cpm: Optional[condecimal(gt=Decimal(0), max_digits=5, decimal_places=2)] = None
