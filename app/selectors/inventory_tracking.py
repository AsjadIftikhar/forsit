from sqlalchemy.orm import Session
from app.database.models import InventoryTracking


def selector_get_inventory_product_tracking(db: Session, product_id: int):
    product_tracking = db.query(InventoryTracking).filter(InventoryTracking.product_id == product_id).order_by(
        InventoryTracking.timestamp).all()

    return product_tracking
