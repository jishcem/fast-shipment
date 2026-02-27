from fastapi import APIRouter, HTTPException

from ..deps import ShipmentServiceDep
from ..schemas.shipment import ShipmentCreate

router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"]
)

@router.post("/")
def create_shipment(shipment_create: ShipmentCreate, service: ShipmentServiceDep):
    return service.create(shipment_create=shipment_create)

@router.get("/all")
def get_all_shipments(service: ShipmentServiceDep):
    return service.get_all()

@router.get("/{id}")
def get_shipment(id: int, service: ShipmentServiceDep):
    shipment = service.get(id=id)

    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    return shipment