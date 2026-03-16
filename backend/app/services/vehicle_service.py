from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


def get_all_vehicles(db: Session) -> list[Vehicle]:
    return db.query(Vehicle).all()


def get_vehicle_by_id(vehicle_id: int, db: Session) -> Vehicle:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojazd o ID {vehicle_id} nie istnieje"
        )
    return vehicle


def get_available_vehicles(db: Session) -> list[Vehicle]:
    return db.query(Vehicle).filter(
        Vehicle.is_available == True,
        Vehicle.status == "available"
    ).all()


def create_vehicle(data: VehicleCreate, db: Session) -> Vehicle:
    existing = db.query(Vehicle).filter(
        Vehicle.plate_number == data.plate_number
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Pojazd z numerem {data.plate_number} już istnieje"
        )

    vehicle = Vehicle(**data.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def update_vehicle(vehicle_id: int, data: VehicleUpdate, db: Session) -> Vehicle:
    vehicle = get_vehicle_by_id(vehicle_id, db)

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(vehicle, field, value)

    db.commit()
    db.refresh(vehicle)
    return vehicle


def delete_vehicle(vehicle_id: int, db: Session) -> dict:
    vehicle = get_vehicle_by_id(vehicle_id, db)
    db.delete(vehicle)
    db.commit()
    return {"message": f"Pojazd {vehicle.plate_number} został usunięty"}