from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.dependencies import get_ticket_service
from app.schemas.ticket import (
    TicketRegisterRequest,
    TicketRegisterResponse,
    TicketUnregisterResponse,
)
from app.services.ticket import TicketService

router = APIRouter(
    prefix="/api/tickets",
    tags=["Tickets"],
)


@router.post(
    "",
    response_model=TicketRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: TicketRegisterRequest,
    service: TicketService = Depends(get_ticket_service),
) -> TicketRegisterResponse:

    ticket_id = await service.register(
        request=request,
    )
    return TicketRegisterResponse(ticket_id=ticket_id)


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_200_OK,
)
async def unregister(
    ticket_id: UUID,
    service: TicketService = Depends(get_ticket_service),
) -> TicketUnregisterResponse:
    await service.unregister(ticket_id)

    return TicketUnregisterResponse(success=True)
