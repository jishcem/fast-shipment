from typing import Annotated

from sqlmodel import Session
from fastapi import Depends

from app.database.session import get_session
from ..services.shipment import ShipmentService

SessionDep = Annotated[Session, Depends(get_session)]

def get_shipment_service(session: SessionDep):
    return ShipmentService(session=session)

ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]