from datetime import datetime
from sqlalchemy.orm import Session

from app.database.models import InventoryTracking


def service_create_inventory_tracking(db: Session, product_id: int, quantity: int):
    inventory_entry = InventoryTracking(product_id=product_id, quantity=quantity, timestamp=datetime.utcnow())
    db.add(inventory_entry)
    db.commit()
    db.refresh(inventory_entry)
    return inventory_entry
