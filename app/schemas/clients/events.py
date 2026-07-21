from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


# Вложенные объекты
class ProviderPlace(BaseModel):
    id: UUID
    name: str
    city: str
    address: str
    seats_pattern: str
    changed_at: datetime
    created_at: datetime

# Основная сущность
class ProviderEvent(BaseModel):
    id: UUID
    name: str
    place: ProviderPlace
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int
    changed_at: datetime
    created_at: datetime
    status_changed_at: datetime

# Контейнер ответа API
class ProviderEventsPage(BaseModel):
    next: str | None
    previous: str | None
    results: list[ProviderEvent]
    
class ProviderSeatsResponse(BaseModel):
    seats: list[str]
    
class ProviderRegistrationRequest(BaseModel):
    first_name: str
    last_name: str
    seat: str
    email: EmailStr

class ProviderRegistrationResponse(BaseModel):
    ticket_id: UUID
    
class ProviderUnregisterRequest(BaseModel):
    ticket_id: UUID


class ProviderUnregisterResponse(BaseModel):
    success: bool