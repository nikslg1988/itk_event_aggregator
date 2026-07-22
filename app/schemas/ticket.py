from uuid import UUID

from pydantic import BaseModel, EmailStr


class TicketRegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    seat: str


class TicketRegisterResponse(BaseModel):
    ticket_id: UUID
