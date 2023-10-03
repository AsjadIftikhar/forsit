from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.selectors.products import selector_get_product
from app.serializers.sales import SaleCreate, SaleRead
from app.services.email import EmailSender
from app.services.inventory_tracking import service_create_inventory_tracking
from app.services.sales import service_create_sale

router = APIRouter()


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
