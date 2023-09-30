from pydantic import BaseModel
from datetime import datetime


class InventoryTrackingRead(BaseModel):
    id: int
    timestamp: datetime
    quantity: int
