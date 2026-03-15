from sqlalchemy import Column, String, Date, Boolean, Enum
import enum
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship


class DriverStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    SICK_LEAVE = "sick_leave"


class LicenseCategory(enum.Enum):
    B = "B"
    C = "C"
    CE = "CE"
    D = "D"


class Driver(BaseModel):
    __tablename__ = "drivers"

    first_name = Column(
        String(50),
        nullable=False
    )

    last_name = Column(
        String(50),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    phone = Column(
        String(20),
        nullable=False
    )

    license_number = Column(
        String(20),
        unique=True,
        nullable=False
    )

    license_category = Column(
        Enum(LicenseCategory),
        nullable=False,
        default=LicenseCategory.C
    )

    license_expiry_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        Enum(DriverStatus),
        nullable=False,
        default=DriverStatus.ACTIVE
    )

    is_available = Column(
        Boolean,
        default=True,
        nullable=False
    )

    routes = relationship(
    "Route",
    back_populates="driver"
    )

    def __repr__(self):
        return f"<Driver {self.first_name} {self.last_name} ({self.status.value})>"