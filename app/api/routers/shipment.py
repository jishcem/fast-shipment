from fastapi import APIRouter, HTTPException

from ..deps import ShipmentServiceDep
from ..schemas.shipment import ShipmentCreate, ShipmentUpdate, ShipmentPatch

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

@router.put("/{id}")
def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ShipmentServiceDep):
    return service.update(id=id, shipment_update=shipment_update)

@router.patch("/{id}")
def patch_shipment(id: int, shipment_patch: ShipmentPatch, service: ShipmentServiceDep):
    return service.patch(id=id, shipment_patch=shipment_patch)

@router.delete("/{id}")
def delete_shipment(id: int, service: ShipmentServiceDep):
    return service.delete(id=id)