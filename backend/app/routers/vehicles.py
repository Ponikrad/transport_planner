from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user, require_admin
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.services import vehicle_service

router = APIRouter(
    prefix="/vehicles",
    tags=["Pojazdy"]
)


@router.get("/", response_model=list[VehicleResponse])
def get_vehicles(db: Session = Depends(get_db)):
    return vehicle_service.get_all_vehicles(db)


@router.get("/available", response_model=list[VehicleResponse])
def get_available_vehicles(db: Session = Depends(get_db)):
    return vehicle_service.get_available_vehicles(db)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    return vehicle_service.get_vehicle_by_id(vehicle_id, db)


@router.post("/", response_model=VehicleResponse, status_code=201)
def create_vehicle(data: VehicleCreate, db: Session = Depends(get_db)):
    return vehicle_service.create_vehicle(data, db)


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(vehicle_id: int, data: VehicleUpdate, db: Session = Depends(get_db)):
    return vehicle_service.update_vehicle(vehicle_id, data, db)


@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return vehicle_service.delete_vehicle(vehicle_id, db)