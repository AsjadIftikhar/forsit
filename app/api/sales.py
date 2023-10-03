from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.selectors.products import selector_get_product
from app.selectors.sales import selector_get_sales_by_filters, TimeIntervals, \
    selector_calculate_revenue_by_interval
from app.serializers.sales import SaleCreate, SaleRead
from app.services.email import EmailSender
from app.services.inventory_tracking import service_create_inventory_tracking
from app.services.sales import service_create_sale
from typing import List, Optional

router = APIRouter()


@router.get("/", response_model=List[SaleRead])
def get_sales_by_filters(
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = Query(0, description="Number of records to skip (for pagination)"),
        limit: int = Query(10, description="Maximum number of records to return (for pagination)"),
        db: Session = Depends(get_db)
):
    sales = selector_get_sales_by_filters(
        db, product_id, category_id, start_date, end_date, skip, limit
    )
    return sales


@router.post("/", response_model=SaleRead)
def create_sale(
        sale_data: SaleCreate,
        product_id: int,
        db: Session = Depends(get_db)
):
    product = selector_get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total = sale_data.quantity * product.price
    revenue = product.margin * total
    remaining_stock = product.stock - sale_data.quantity

    sale = service_create_sale(db, sale_data, total=total, revenue=revenue, product_id=product_id)
    service_create_inventory_tracking(db, product_id, remaining_stock)

    if remaining_stock < 10:
        email_subject = "Low Stock Alert"
        email_message = f"Product {product.name} is running low on stock. Remaining stock: {remaining_stock}"
        email_sender = EmailSender()
        email_sender.send_email(email_subject, email_message, ["iftikharasjad@gmail.com"])

    return sale


@router.get("/analyze", response_model=float)
def analyze_sales_revenue_by_interval(
        interval: TimeIntervals = Query(..., description="Time interval for revenue analysis"),
        db: Session = Depends(get_db)
):
    total_revenue = selector_calculate_revenue_by_interval(db, interval)

    return total_revenue or 0.0
