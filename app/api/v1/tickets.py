from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.dependencies import get_ticket_service
from app.schemas.ticket import (
    TicketRegisterRequest,
    TicketRegisterResponse,
)
from app.services.ticket import TicketService

router = APIRouter(
    prefix="/api/events",
    tags=["Tickets"],
)


@router.post(
    "/{event_id}/register/",
    response_model=TicketRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    event_id: UUID,
    request: TicketRegisterRequest,
    service: TicketService = Depends(get_ticket_service),
) -> TicketRegisterResponse:
    ticket_id = await service.register(
        event_id=event_id,
        request=request,
    )
    return TicketRegisterResponse(ticket_id=ticket_id)


@router.delete(
    "/{event_id}/unregister/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unregister(
    event_id: UUID,
    service: TicketService = Depends(get_ticket_service),
) -> None:
    await service.unregister(event_id)
