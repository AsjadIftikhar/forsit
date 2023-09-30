from pydantic import BaseModel

from app.serializers.categories import CategoryRead


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    margin: float
    stock: int
    category_id: int


class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    margin: float
    stock: int
    category_id: int


class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    margin: float
    stock: int
    category: CategoryRead


class ProductUpdateStock(BaseModel):
    stock: int
