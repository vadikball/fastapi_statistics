from abc import abstractmethod
from decimal import Decimal, ROUND_UP
from uuid import uuid4

from sqlalchemy import Column, Integer, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID

from db.base import Base


class StatModel(Base):
    __tablename__ = "stats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    date = Column(Date)
    views = Column(Integer, nullable=True)
    clicks = Column(Integer, nullable=True)
    cost = Column(Numeric(5, 2), nullable=True)

    def dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)

        if self.cost is not None:
            if self.clicks is not None:
                d['cpc'] = (self.cost / self.clicks).quantize(Decimal('.01'), rounding=ROUND_UP)
            if self.views is not None:
                d['cpm'] = ((self.cost / self.views) * 1000).quantize(Decimal('.01'), rounding=ROUND_UP)

        return d

