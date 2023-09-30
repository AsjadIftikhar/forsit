from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models import Sale
from app.serializers.sales import SaleCreate


def service_create_sale(db: Session, sale_data: SaleCreate, total: float, revenue: float, product_id: int):
    sale = Sale(**sale_data.model_dump(), sale_date=datetime.utcnow(), total=total, revenue=revenue,
                product_id=product_id)
    db.add(sale)
    db.commit()
    db.refresh(sale)

    return sale
