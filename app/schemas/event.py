from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class EventListResponse(BaseModel):
    count: int
    next: int | None
    previous: int | None
    results: list[EventResponse]
