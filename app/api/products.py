from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.selectors.products import selector_get_products, selector_get_product
from app.services.inventory_tracking import service_create_inventory_tracking
from app.services.products import service_create_product, service_delete_product, service_update_product
from app.serializers.products import ProductCreate, ProductRead, ProductUpdate, ProductUpdateStock

router = APIRouter()


@router.get("/", response_model=list[ProductRead])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = selector_get_products(db, skip=skip, limit=limit)
    return products


@router.post("/", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return service_create_product(db, product)


@router.put("/{product_id}", response_model=ProductUpdate)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = selector_get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_product = service_update_product(db, product, product_update)
    return updated_product


@router.delete("/{product_id}", response_model=None)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = selector_get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    service_delete_product(db, product)
    return Response(status_code=204)


@router.patch("/update_stock/{product_id}", response_model=ProductUpdate)
def update_stock(product_id: int, product_update: ProductUpdateStock, db: Session = Depends(get_db)):
    if product_update.stock <= 0:
        raise HTTPException(status_code=400, detail="Stock value must be greater than 0")

    product = selector_get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product_update.stock += product.stock
    updated_product = service_update_product(db, product, product_update)

    service_create_inventory_tracking(db, product_id, product.stock)

    return updated_product
