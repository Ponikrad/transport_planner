from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional
from app.models.driver import DriverStatus, LicenseCategory


class DriverCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    license_number: str
    license_category: LicenseCategory = LicenseCategory.C
    license_expiry_date: date
    status: DriverStatus = DriverStatus.ACTIVE

    @field_validator("license_expiry_date")
    def license_must_be_valid(cls, v):
        if v < date.today():
            raise ValueError("Prawo jazdy jest przeterminowane!")
        return v


class DriverUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None
    license_category: Optional[LicenseCategory] = None
    license_expiry_date: Optional[date] = None
    status: Optional[DriverStatus] = None


class DriverResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    license_number: str
    license_category: LicenseCategory
    license_expiry_date: date
    status: DriverStatus
    is_available: bool

    class Config:
        from_attributes = True