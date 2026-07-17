from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class EventSchema(BaseModel):
    id: UUID
    place_id: UUID
    name: str
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int
    changed_at: datetime
    created_at: datetime
    status_changed_at: datetime
        