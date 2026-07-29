from uuid import UUID

from pydantic import BaseModel, EmailStr


class TicketRegisterRequest(BaseModel):
    event_id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    seat: str


class TicketRegisterResponse(BaseModel):
    ticket_id: UUID


class AvailableSeatsResponse(BaseModel):
    event_id: UUID
    available_seats: list[str]


class TicketUnregisterResponse(BaseModel):
    success: bool
