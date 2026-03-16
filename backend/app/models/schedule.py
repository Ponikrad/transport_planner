from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Date, Time, Boolean, Text
from sqlalchemy.orm import relationship
import enum
from app.models.base_model import BaseModel


class ShiftType(enum.Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"
    CUSTOM = "custom"


class ScheduleStatus(enum.Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Schedule(BaseModel):
    __tablename__ = "schedules"

    driver_id = Column(
        Integer,
        ForeignKey("drivers.id"),
        nullable=False
    )

    work_date = Column(Date, nullable=False)

    shift_start = Column(String(5), nullable=False)
    shift_end = Column(String(5), nullable=False)

    shift_type = Column(
        Enum(ShiftType),
        nullable=False,
        default=ShiftType.CUSTOM
    )

    status = Column(
        Enum(ScheduleStatus),
        nullable=False,
        default=ScheduleStatus.DRAFT
    )

    route_id = Column(
        Integer,
        ForeignKey("routes.id"),
        nullable=True
    )

    notes = Column(Text, nullable=True)

    is_day_off = Column(Boolean, default=False, nullable=False)
    day_off_reason = Column(String(100), nullable=True)

    driver = relationship("Driver", back_populates="schedules")
    route = relationship("Route")

    def __repr__(self):
        return f"<Schedule {self.driver_id} {self.work_date} {self.shift_start}-{self.shift_end}>"