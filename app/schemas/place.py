from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class PlaceResponse(BaseModel):
    id: UUID
    name: str
    city: str
    address: str
    seats_pattern: str
    changed_at: datetime
    created_at: datetime
