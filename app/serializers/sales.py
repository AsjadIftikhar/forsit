import datetime

from pydantic import BaseModel

from app.serializers.products import ProductRead


class SaleCreate(BaseModel):
    quantity: int


class SaleRead(BaseModel):
    id: int
    quantity: int
    sale_date: datetime.datetime
    total: float
    revenue: float
    product: ProductRead
