from fastapi import APIRouter, HTTPException

from ..deps import ShipmentServiceDep
from ..schemas.shipment import ShipmentCreate, ShipmentUpdate, ShipmentPatch

router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"]
)

@router.post("/")
async def create_shipment(shipment_create: ShipmentCreate, service: ShipmentServiceDep):
    return await service.create(shipment_create=shipment_create)

@router.get("/all")
async def get_all_shipments(service: ShipmentServiceDep):
    return await service.get_all()

@router.get("/{id}")
async def get_shipment(id: int, service: ShipmentServiceDep):
    shipment = await service.get(id=id)

    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    return shipment

@router.put("/{id}")
async def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ShipmentServiceDep):
    return await service.update(id=id, shipment_update=shipment_update)

@router.patch("/{id}")
async def patch_shipment(id: int, shipment_patch: ShipmentPatch, service: ShipmentServiceDep):
    return await service.patch(id=id, shipment_patch=shipment_patch)

@router.delete("/{id}")
async def delete_shipment(id: int, service: ShipmentServiceDep):
    return await service.delete(id=id)