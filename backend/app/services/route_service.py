from sqlalchemy.orm import Session, joinedload

from fastapi import HTTPException, status
from app.models.route import Route
from app.models.driver import Driver, DriverStatus
from app.models.vehicle import Vehicle, VehicleStatus
from app.schemas.route import RouteCreate, RouteUpdate
from app.services.scheduling_service import check_driver_conflicts, check_vehicle_conflicts


def get_all_routes(db: Session) -> list[Route]:
    return db.query(Route).options(
        joinedload(Route.driver),
        joinedload(Route.vehicle)
    ).all()


def get_route_by_id(route_id: int, db: Session) -> Route:
    route = db.query(Route).options(
        joinedload(Route.driver),
        joinedload(Route.vehicle)
    ).filter(Route.id == route_id).first()

    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trasa o ID {route_id} nie istnieje"
        )
    return route


def create_route(data: RouteCreate, db: Session) -> Route:

    driver = db.query(Driver).filter(Driver.id == data.driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Kierowca nie istnieje")
    if driver.status != DriverStatus.ACTIVE:
        raise HTTPException(
            status_code=400,
            detail=f"Kierowca {driver.first_name} {driver.last_name} nie jest aktywny!"
        )

    vehicle = db.query(Vehicle).filter(Vehicle.id == data.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Pojazd nie istnieje")
    if vehicle.status == VehicleStatus.SERVICE:
        raise HTTPException(
            status_code=400,
            detail=f"Pojazd {vehicle.plate_number} jest w serwisie!"
        )

    check_driver_conflicts(data.driver_id, data.planned_start, data.planned_end, db)
    check_vehicle_conflicts(data.vehicle_id, data.planned_start, data.planned_end, db)

    route = Route(**data.model_dump())
    db.add(route)
    db.commit()
    db.refresh(route)

    return get_route_by_id(route.id, db)


def update_route(route_id: int, data: RouteUpdate, db: Session) -> Route:
    route = get_route_by_id(route_id, db)

    updates = data.model_dump(exclude_unset=True)

    # Jeśli zmieniamy czas — sprawdamy konflikty ponownie
    new_start = updates.get("planned_start", route.planned_start)
    new_end = updates.get("planned_end", route.planned_end)

    if "planned_start" in updates or "planned_end" in updates:
        check_driver_conflicts(route.driver_id, new_start, new_end, db, exclude_route_id=route_id)
        check_vehicle_conflicts(route.vehicle_id, new_start, new_end, db, exclude_route_id=route_id)

    for field, value in updates.items():
        setattr(route, field, value)

    db.commit()
    db.refresh(route)
    return get_route_by_id(route_id, db)


def delete_route(route_id: int, db: Session) -> dict:
    route = get_route_by_id(route_id, db)
    db.delete(route)
    db.commit()
    return {"message": f"Trasa {route.origin} → {route.destination} została usunięta"}