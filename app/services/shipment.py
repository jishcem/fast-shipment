from datetime import datetime, timedelta

from sqlmodel import Session, select
from fastapi import HTTPException, status

from ..database.models import Shipment, ShipmentStatus
from ..api.schemas.shipment import ShipmentCreate, ShipmentUpdate, ShipmentPatch

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
    
    def update(self, id: int, shipment_update: ShipmentUpdate) -> Shipment:
        shipment = self.get(id)

        if shipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No shipment found")

        shipment.sqlmodel_update(shipment_update)
        self.session.add(shipment)
        self.session.commit()
        self.session.refresh(shipment)
        return shipment
    
    def patch(self, id: int, shipment_patch: ShipmentPatch):
        shipment = self.get(id)

        if shipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No shipment found")

        shipment.sqlmodel_update(shipment_patch.model_dump(exclude_unset=True))
        self.session.add(shipment)
        self.session.commit()
        self.session.refresh(shipment)
        return shipment
    
    def delete(self, id: int) -> None:
        shipment = self.get(id)

        if shipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No shipment found")
        
        self.session.delete(shipment)
        self.session.commit()