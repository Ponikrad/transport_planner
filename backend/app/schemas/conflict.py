from pydantic import BaseModel
from typing import Optional
from app.models.conflict import ConflictType, ConflictStatus


class ConflictResponse(BaseModel):
    id: int
    conflict_type: ConflictType
    status: ConflictStatus
    driver_id: Optional[int]
    vehicle_id: Optional[int]
    route_id: Optional[int]
    description: str
    resolved_note: Optional[str]

    class Config:
        from_attributes = True


class ConflictResolve(BaseModel):
    resolved_note: str