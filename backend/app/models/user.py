from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from app.models.base_model import BaseModel


class UserRole(enum.Enum):
    ADMIN = "admin"
    DISPATCHER = "dispatcher"
    VIEWER = "viewer"


class User(BaseModel):
    """
    Użytkownik != Kierowca!
    Użytkownik - dyspozytor, admin.
    Kierowca to obiekt który jest planowany.
    """

    __tablename__ = "users"

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(String(255), nullable=False)

    full_name = Column(String(100), nullable=True)

    role = Column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.DISPATCHER
    )

    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username} ({self.role.value})>"