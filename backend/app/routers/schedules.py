from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from app.core.dependencies import get_db, get_current_user, require_admin
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from app.services import schedule_service

router = APIRouter(
    prefix="/schedules",
    tags=["Grafiki"]
)


@router.get("/", response_model=list[ScheduleResponse])
def get_schedules(
    start_date: Optional[date] = Query(None, description="Od kiedy"),
    end_date: Optional[date] = Query(None, description="Do kiedy"),
    driver_id: Optional[int] = Query(None, description="ID kierowcy"),
    db: Session = Depends(get_db)
):

    if driver_id:
        return schedule_service.get_schedules_by_driver(driver_id, db)
    if start_date and end_date:
        return schedule_service.get_schedules_by_date_range(start_date, end_date, db)
    return schedule_service.get_all_schedules(db)


@router.post("/", response_model=ScheduleResponse, status_code=201)
def create_schedule(data: ScheduleCreate, db: Session = Depends(get_db)):
    return schedule_service.create_schedule(data, db)


@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(
    schedule_id: int,
    data: ScheduleUpdate,
    db: Session = Depends(get_db)
):
    return schedule_service.update_schedule(schedule_id, data, db)


@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return schedule_service.delete_schedule(schedule_id, db)