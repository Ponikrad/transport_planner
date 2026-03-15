from pydantic import BaseModel, field_validator, model_validator

from typing import Optional
from datetime import datetime
from app.models.route import RouteStatus
from app.schemas.driver import DriverResponse
from app.schemas.vehicle import VehicleResponse


class RouteCreate(BaseModel):
    driver_id: int
    vehicle_id: int
    origin: str
    destination: str
    waypoints: Optional[str] = None
    distance_km: Optional[float] = None
    planned_start: datetime
    planned_end: datetime
    cargo_description: Optional[str] = None
    cargo_weight_kg: Optional[float] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def end_must_be_after_start(self):
        if self.planned_end <= self.planned_start:
            raise ValueError("Koniec trasy musi być późniejszy niż początek!")
        return self

    @model_validator(mode="after")
    def max_route_duration(self):
        duration = (self.planned_end - self.planned_start).total_seconds() / 3600
        if duration > 16:
            raise ValueError(f"Trasa nie może trwać dłużej niż 16h! (podano {duration:.1f}h)")
        return self


class RouteUpdate(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    waypoints: Optional[str] = None
    distance_km: Optional[float] = None
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    cargo_description: Optional[str] = None
    cargo_weight_kg: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[RouteStatus] = None


class RouteResponse(BaseModel):
    id: int
    driver_id: int
    vehicle_id: int
    origin: str
    destination: str
    waypoints: Optional[str]
    distance_km: Optional[float]
    planned_start: datetime
    planned_end: datetime
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    cargo_description: Optional[str]
    cargo_weight_kg: Optional[float]
    notes: Optional[str]
    status: RouteStatus

    driver: Optional[DriverResponse] = None
    vehicle: Optional[VehicleResponse] = None

    class Config:
        from_attributes = True