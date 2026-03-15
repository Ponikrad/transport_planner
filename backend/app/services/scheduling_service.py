from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.models.route import Route, RouteStatus
from app.models.driver import Driver
from app.models.vehicle import Vehicle


def check_driver_conflicts(
    driver_id: int,
    planned_start: datetime,
    planned_end: datetime,
    db: Session,
    exclude_route_id: int = None
) -> None:
    
    # Pobierz wszystkie aktywne trasy kierowcy w tym samym dniu, które kolidują czasowo
    query = db.query(Route).filter(
        Route.driver_id == driver_id,
        Route.status != RouteStatus.CANCELLED,
        Route.planned_start < planned_end,
        Route.planned_end > planned_start
    )

    # Przy aktualizacji pomijamy samą siebie
    if exclude_route_id:
        query = query.filter(Route.id != exclude_route_id)

    conflicting_route = query.first()

    if conflicting_route:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Konflikt! Kierowca ma już trasę "
                f"{conflicting_route.origin} → {conflicting_route.destination} "
                f"w godzinach {conflicting_route.planned_start.strftime('%H:%M')} "
                f"- {conflicting_route.planned_end.strftime('%H:%M')}"
            )
        )

    # Sprawdaamy łączny czas pracy w danym dniu
    day_start = planned_start.replace(hour=0, minute=0, second=0)
    day_end = planned_start.replace(hour=23, minute=59, second=59)

    day_routes = db.query(Route).filter(
        Route.driver_id == driver_id,
        Route.status != RouteStatus.CANCELLED,
        Route.planned_start >= day_start,
        Route.planned_start <= day_end
    ).all()

    total_hours = sum(
        (r.planned_end - r.planned_start).total_seconds() / 3600
        for r in day_routes
    )
    new_route_hours = (planned_end - planned_start).total_seconds() / 3600
    total_hours += new_route_hours

    if total_hours > 16:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Przekroczono limit 16h pracy dziennie! "
                f"Kierowca ma już {total_hours - new_route_hours:.1f}h, "
                f"nowa trasa doda {new_route_hours:.1f}h "
                f"(łącznie {total_hours:.1f}h)"
            )
        )


def check_vehicle_conflicts(
    vehicle_id: int,
    planned_start: datetime,
    planned_end: datetime,
    db: Session,
    exclude_route_id: int = None
) -> None:
    query = db.query(Route).filter(
        Route.vehicle_id == vehicle_id,
        Route.status != RouteStatus.CANCELLED,
        Route.planned_start < planned_end,
        Route.planned_end > planned_start
    )

    if exclude_route_id:
        query = query.filter(Route.id != exclude_route_id)

    conflicting_route = query.first()

    if conflicting_route:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Konflikt! Pojazd jest już zajęty trasą "
                f"{conflicting_route.origin} → {conflicting_route.destination} "
                f"w godzinach {conflicting_route.planned_start.strftime('%H:%M')} "
                f"- {conflicting_route.planned_end.strftime('%H:%M')}"
            )
        )