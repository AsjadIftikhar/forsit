from fastapi import FastAPI
from app.api import categories, products, inventory_tracking, sales

app = FastAPI()

app.include_router(categories.router, prefix="/categories", tags=["Category"])
app.include_router(products.router, prefix="/products", tags=["Product"])
app.include_router(inventory_tracking.router, prefix="/inventory", tags=["InventoryTracking"])
app.include_router(sales.router, prefix="/sales", tags=["Sale"])
