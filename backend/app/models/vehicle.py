from sqlalchemy import Column, String, Integer, Float, Boolean, Enum
import enum
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship


class VehicleStatus(enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    SERVICE = "service"
    INACTIVE = "inactive"


class VehicleType(enum.Enum):
    TRUCK = "truck"
    VAN = "van"
    SEMI = "semi"
    REFRIGERATED = "refrigerated"


class Vehicle(BaseModel):

    __tablename__ = "vehicles"

    plate_number = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)

    year = Column(Integer, nullable=True)   

    vehicle_type = Column(
        Enum(VehicleType),
        nullable=False,
        default=VehicleType.TRUCK
    )

    max_load_kg = Column(
        Float,
        nullable=True
    )

    max_load_volume_m3 = Column(
        Float,
        nullable=True
    )

    fuel_consumption_per_100km = Column(
        Float,
        nullable=True
    )

    last_service_date = Column(
        String(20),
        nullable=True
    )

    next_service_date = Column(
        String(20),
        nullable=True
    )

    status = Column(
        Enum(VehicleStatus),
        nullable=False,
        default=VehicleStatus.AVAILABLE
    )

    is_available = Column(
        Boolean,
        default=True,
        nullable=False
    )

    routes = relationship(
    "Route",
    back_populates="vehicle"
    )

    def __repr__(self):
        return f"<Vehicle {self.plate_number} {self.brand} {self.model} ({self.status.value})>"