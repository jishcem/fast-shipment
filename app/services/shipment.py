from datetime import datetime, timedelta

from sqlmodel import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Shipment, ShipmentStatus
from ..api.schemas.shipment import ShipmentCreate, ShipmentUpdate, ShipmentPatch

class ShipmentService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Shipment]:
        result = await self.session.execute(select(Shipment))
        shipments = result.scalars().all()
        return shipments
    
    async def get(self, id) -> Shipment:
        return await self.session.get(Shipment, id)

    async def create(self, shipment_create: ShipmentCreate) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=7)
        )        

        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment
    
    async def update(self, id: int, shipment_update: ShipmentUpdate) -> Shipment:
        shipment = await self.get(id)

        if shipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No shipment found")

        shipment.sqlmodel_update(shipment_update)
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment
    
    async def patch(self, id: int, shipment_patch: ShipmentPatch):
        shipment = await self.get(id)

        if shipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No shipment found")

        shipment.sqlmodel_update(shipment_patch.model_dump(exclude_unset=True))
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment
    
    async def delete(self, id: int) -> None:
        shipment = await self.get(id)

        if shipment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No shipment found")
        
        await self.session.delete(shipment)
        await self.session.commit()