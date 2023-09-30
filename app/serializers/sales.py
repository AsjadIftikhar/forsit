import datetime

from pydantic import BaseModel


class SaleCreate(BaseModel):
    quantity: int


class SaleRead(BaseModel):
    id: int
    quantity: int
    sale_date: datetime.datetime
    total: float
    revenue: float
