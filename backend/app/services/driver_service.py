from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.driver import Driver
from app.schemas.driver import DriverCreate, DriverUpdate


def get_all_drivers(db: Session) -> list[Driver]:
    return db.query(Driver).all()


def get_driver_by_id(driver_id: int, db: Session) -> Driver:
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kierowca o ID {driver_id} nie istnieje"
        )
    return driver


def create_driver(data: DriverCreate, db: Session) -> Driver:
    existing = db.query(Driver).filter(Driver.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Kierowca z emailem {data.email} już istnieje"
        )

    existing_license = db.query(Driver).filter(
        Driver.license_number == data.license_number
    ).first()
    if existing_license:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Prawo jazdy {data.license_number} już jest w systemie"
        )

    driver = Driver(**data.model_dump())

    db.add(driver)
    db.commit()
    db.refresh(driver)

    return driver


def update_driver(driver_id: int, data: DriverUpdate, db: Session) -> Driver:
    driver = get_driver_by_id(driver_id, db)
    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(driver, field, value)

    db.commit()
    db.refresh(driver)
    return driver


def delete_driver(driver_id: int, db: Session) -> dict:
    driver = get_driver_by_id(driver_id, db)

    db.delete(driver)
    db.commit()

    return {"message": f"Kierowca {driver.first_name} {driver.last_name} został usunięty"}