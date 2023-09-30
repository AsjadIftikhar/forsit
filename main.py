from fastapi import FastAPI
from app.api import categories, products

app = FastAPI()

app.include_router(categories.router, prefix="/categories", tags=["Category"])
app.include_router(products.router, prefix="/products", tags=["Product"])

