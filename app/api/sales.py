from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.selectors.products import selector_get_product
from app.serializers.sales import SaleCreate, SaleRead
from app.services.sales import service_create_sale

router = APIRouter()


@router.post("/", response_model=SaleRead)
def create_sale(sale_data: SaleCreate, product_id: int, db: Session = Depends(get_db)):
    product = selector_get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total = sale_data.quantity * product.price
    revenue = product.margin * total

    sale = service_create_sale(db, sale_data, total=total, revenue=revenue, product_id=product_id)
    return sale
