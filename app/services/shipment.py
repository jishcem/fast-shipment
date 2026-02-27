from datetime import datetime, timedelta

from sqlmodel import Session, select

from ..database.models import Shipment, ShipmentStatus
from ..api.schemas.shipment import ShipmentCreate

class ShipmentService():
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Shipment]:
        return self.session.exec(select(Shipment)).all()
    
    def get(self, id) -> Shipment:
        return self.session.get(Shipment, id)

    def create(self, shipment_create: ShipmentCreate) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=7)
        )        

        self.session.add(new_shipment)
        self.session.commit()
        self.session.refresh(new_shipment)
        return new_shipment