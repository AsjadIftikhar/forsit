from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.selectors.inventory_tracking import selector_get_inventory_product_tracking
from app.serializers.inventory_tracking import InventoryTrackingRead

router = APIRouter()


@router.get("/tracking/{product_id}", response_model=List[InventoryTrackingRead])
def get_inventory_product_tracking(product_id: int, db: Session = Depends(get_db)):
    inventory_product_tracking = selector_get_inventory_product_tracking(db, product_id)

    product_trackings = [
        InventoryTrackingRead(id=tracking.id, timestamp=tracking.timestamp.date(), quantity=tracking.quantity)
        for tracking in inventory_product_tracking
    ]

    return product_trackings
