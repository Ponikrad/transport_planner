from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user, require_admin
from app.schemas.driver import DriverCreate, DriverUpdate, DriverResponse
from app.services import driver_service

router = APIRouter(
    prefix="/drivers",
    tags=["Kierowcy"]
)


@router.get("/", response_model=list[DriverResponse])
def get_drivers(db: Session = Depends(get_db)):
    return driver_service.get_all_drivers(db)


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    return driver_service.get_driver_by_id(driver_id, db)


@router.post("/", response_model=DriverResponse, status_code=201)
def create_driver(data: DriverCreate, db: Session = Depends(get_db)):
    return driver_service.create_driver(data, db)


@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id: int, data: DriverUpdate, db: Session = Depends(get_db)):
    return driver_service.update_driver(driver_id, data, db)


@router.delete("/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return driver_service.delete_driver(driver_id, db)