from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
import enum
from app.models.base_model import BaseModel


class ConflictType(enum.Enum):
    DRIVER_OVERLAP = "driver_overlap"
    VEHICLE_OVERLAP = "vehicle_overlap"
    MAX_HOURS_EXCEEDED = "max_hours_exceeded"
    MISSING_BREAK = "missing_break"
    REST_VIOLATION = "rest_violation"
    LICENSE_EXPIRED = "license_expired"


class ConflictStatus(enum.Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    IGNORED = "ignored"


class Conflict(BaseModel):
    __tablename__ = "conflicts"

    conflict_type = Column(Enum(ConflictType), nullable=False)
    status = Column(
        Enum(ConflictStatus),
        nullable=False,
        default=ConflictStatus.ACTIVE
    )

    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)

    description = Column(Text, nullable=False)
    resolved_note = Column(Text, nullable=True)

    driver = relationship("Driver")
    vehicle = relationship("Vehicle")
    route = relationship("Route")

    def __repr__(self):
        return f"<Conflict {self.conflict_type.value} ({self.status.value})>"