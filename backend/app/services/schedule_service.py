from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from datetime import date, datetime, timedelta
from app.models.schedule import Schedule, ScheduleStatus
from app.models.conflict import Conflict, ConflictType, ConflictStatus
from app.models.driver import Driver, DriverStatus
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate


def get_all_schedules(db: Session) -> list[Schedule]:
    return db.query(Schedule).options(
        joinedload(Schedule.driver)
    ).all()


def get_schedules_by_driver(driver_id: int, db: Session) -> list[Schedule]:
    return db.query(Schedule).filter(
        Schedule.driver_id == driver_id
    ).order_by(Schedule.work_date).all()


def get_schedules_by_date_range(
    start_date: date,
    end_date: date,
    db: Session
) -> list[Schedule]:
    return db.query(Schedule).options(
        joinedload(Schedule.driver)
    ).filter(
        Schedule.work_date >= start_date,
        Schedule.work_date <= end_date
    ).order_by(Schedule.work_date).all()


def _time_str_to_minutes(time_str: str) -> int:
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes


def _check_schedule_conflicts(
    driver_id: int,
    work_date: date,
    shift_start: str,
    shift_end: str,
    db: Session,
    exclude_id: int = None
) -> None:
    existing = db.query(Schedule).filter(
        Schedule.driver_id == driver_id,
        Schedule.work_date == work_date,
        Schedule.status != ScheduleStatus.CANCELLED,
        Schedule.is_day_off == False
    )

    if exclude_id:
        existing = existing.filter(Schedule.id != exclude_id)

    existing = existing.all()

    new_start = _time_str_to_minutes(shift_start)
    new_end = _time_str_to_minutes(shift_end)

    for schedule in existing:
        existing_start = _time_str_to_minutes(schedule.shift_start)
        existing_end = _time_str_to_minutes(schedule.shift_end)

        if new_start < existing_end and new_end > existing_start:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Konflikt grafiku! Kierowca ma już zmianę "
                    f"{schedule.shift_start}-{schedule.shift_end} "
                    f"w dniu {work_date}"
                )
            )

    previous_day = work_date - timedelta(days=1)
    previous_schedules = db.query(Schedule).filter(
        Schedule.driver_id == driver_id,
        Schedule.work_date == previous_day,
        Schedule.status != ScheduleStatus.CANCELLED,
        Schedule.is_day_off == False
    ).all()

    for prev in previous_schedules:
        prev_end_minutes = _time_str_to_minutes(prev.shift_end)
        # Minuty od północy do końca poprzedniej zmiany
        # + minuty do początku nowej zmiany (następny dzień = +1440 minut)
        rest_minutes = (1440 - prev_end_minutes) + new_start
        rest_hours = rest_minutes / 60

        if rest_hours < 11:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Za mało odpoczynku między zmianami! "
                    f"Poprzednia zmiana kończy się {prev.shift_end}, "
                    f"nowa zaczyna {shift_start}. "
                    f"Odpoczynek: {rest_hours:.1f}h (wymagane min. 11h)"
                )
            )


def create_schedule(data: ScheduleCreate, db: Session) -> Schedule:
    """Tworzy wpis w grafiku"""

    driver = db.query(Driver).filter(Driver.id == data.driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Kierowca nie istnieje")
    if driver.status == DriverStatus.INACTIVE:
        raise HTTPException(
            status_code=400,
            detail=f"Kierowca {driver.first_name} {driver.last_name} jest nieaktywny!"
        )

    if not data.is_day_off:
        _check_schedule_conflicts(
            data.driver_id,
            data.work_date,
            data.shift_start,
            data.shift_end,
            db
        )

    schedule = Schedule(**data.model_dump())
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


def update_schedule(schedule_id: int, data: ScheduleUpdate, db: Session) -> Schedule:
    """Aktualizuje wpis w grafiku"""
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Wpis w grafiku nie istnieje")

    updates = data.model_dump(exclude_unset=True)

    new_start = updates.get("shift_start", schedule.shift_start)
    new_end = updates.get("shift_end", schedule.shift_end)
    new_date = updates.get("work_date", schedule.work_date)

    if any(k in updates for k in ["shift_start", "shift_end", "work_date"]):
        _check_schedule_conflicts(
            schedule.driver_id, new_date, new_start, new_end,
            db, exclude_id=schedule_id
        )

    for field, value in updates.items():
        setattr(schedule, field, value)

    db.commit()
    db.refresh(schedule)
    return schedule


def delete_schedule(schedule_id: int, db: Session) -> dict:
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Wpis w grafiku nie istnieje")
    db.delete(schedule)
    db.commit()
    return {"message": "Wpis w grafiku został usunięty"}