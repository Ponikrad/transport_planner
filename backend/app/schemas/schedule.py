from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import date
from app.models.schedule import ShiftType, ScheduleStatus


class ScheduleCreate(BaseModel):
    driver_id: int
    work_date: date
    shift_start: str
    shift_end: str
    shift_type: ShiftType = ShiftType.CUSTOM
    route_id: Optional[int] = None
    notes: Optional[str] = None
    is_day_off: bool = False
    day_off_reason: Optional[str] = None

    @field_validator("shift_start", "shift_end")
    def validate_time_format(cls, v):
        try:
            parts = v.split(":")
            assert len(parts) == 2
            hours, minutes = int(parts[0]), int(parts[1])
            assert 0 <= hours <= 23
            assert 0 <= minutes <= 59
        except (ValueError, AssertionError):
            raise ValueError(f"Nieprawidłowy format godziny '{v}'. Użyj HH:MM np. '08:00'")
        return v

    @model_validator(mode="after")
    def day_off_validation(self):
        if self.is_day_off and self.route_id:
            raise ValueError("Dzień wolny nie może mieć przypisanej trasy!")
        if self.is_day_off and not self.day_off_reason:
            raise ValueError("Podaj powód dnia wolnego (np. 'urlop', 'chorobowe')")
        return self


class ScheduleUpdate(BaseModel):
    work_date: Optional[date] = None
    shift_start: Optional[str] = None
    shift_end: Optional[str] = None
    shift_type: Optional[ShiftType] = None
    status: Optional[ScheduleStatus] = None
    route_id: Optional[int] = None
    notes: Optional[str] = None
    is_day_off: Optional[bool] = None
    day_off_reason: Optional[str] = None


class ScheduleResponse(BaseModel):
    id: int
    driver_id: int
    work_date: date
    shift_start: str
    shift_end: str
    shift_type: ShiftType
    status: ScheduleStatus
    route_id: Optional[int]
    notes: Optional[str]
    is_day_off: bool
    day_off_reason: Optional[str]

    class Config:
        from_attributes = True