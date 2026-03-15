from pydantic import BaseModel, field_validator
from typing import Optional
from app.models.vehicle import VehicleStatus, VehicleType


class VehicleCreate(BaseModel):
    plate_number: str
    brand: str
    model: str
    year: Optional[int] = None
    vehicle_type: VehicleType = VehicleType.TRUCK
    max_load_kg: Optional[float] = None
    max_load_volume_m3: Optional[float] = None
    fuel_consumption_per_100km: Optional[float] = None
    last_service_date: Optional[str] = None
    next_service_date: Optional[str] = None
    status: VehicleStatus = VehicleStatus.AVAILABLE

    @field_validator("year")
    def year_must_be_valid(cls, v):
        if v is not None and (v < 1990 or v > 2026):
            raise ValueError("Rok produkcji musi być między 1990 a 2026")
        return v

    @field_validator("plate_number")
    def plate_must_be_uppercase(cls, v):
        return v.upper().strip()


class VehicleUpdate(BaseModel):
    plate_number: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    vehicle_type: Optional[VehicleType] = None
    max_load_kg: Optional[float] = None
    max_load_volume_m3: Optional[float] = None
    fuel_consumption_per_100km: Optional[float] = None
    last_service_date: Optional[str] = None
    next_service_date: Optional[str] = None
    status: Optional[VehicleStatus] = None
    is_available: Optional[bool] = None


class VehicleResponse(BaseModel):
    id: int
    plate_number: str
    brand: str
    model: str
    year: Optional[int]
    vehicle_type: VehicleType
    max_load_kg: Optional[float]
    max_load_volume_m3: Optional[float]
    fuel_consumption_per_100km: Optional[float]
    last_service_date: Optional[str]
    next_service_date: Optional[str]
    status: VehicleStatus
    is_available: bool

    class Config:
        from_attributes = True