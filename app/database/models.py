from enum import Enum
from datetime import datetime

from sqlmodel import SQLModel, Field


class ShipmentStatus(str, Enum):
    placed = "placed"
    shipped = "shipped"
    in_transit = "in_transit"
    delivered = "delivered"
    returned = "returned"

class Shipment(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    content: str
    weight: float
    destination: int | None
    status: ShipmentStatus
    estimated_delivery: datetime