from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
import enum
from app.models.base_model import BaseModel


class RouteStatus(enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Route(BaseModel):
    __tablename__ = "routes"
    driver_id = Column(
        Integer,
        ForeignKey("drivers.id"),
        nullable=False
    )

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    origin = Column(String(200), nullable=False)
    destination = Column(String(200), nullable=False)

    waypoints = Column(Text, nullable=True)

    distance_km = Column(Float, nullable=True)

    planned_start = Column(DateTime(timezone=True), nullable=False)
    planned_end = Column(DateTime(timezone=True), nullable=False)

    # Rzeczywisty czas — wypełniają się gdy trasa się rozpocznie/skończy
    actual_start = Column(DateTime(timezone=True), nullable=True)
    actual_end = Column(DateTime(timezone=True), nullable=True)

    cargo_description = Column(String(500), nullable=True)
    cargo_weight_kg = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

    status = Column(
        Enum(RouteStatus),
        nullable=False,
        default=RouteStatus.PLANNED
    )

    driver = relationship(
        "Driver",
        back_populates="routes"
    )

    vehicle = relationship(
        "Vehicle",
        back_populates="routes"
    )

    def __repr__(self):
        return f"<Route {self.origin} → {self.destination} ({self.status.value})>"