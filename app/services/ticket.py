from uuid import UUID

from app.clients.events import EventsProviderClient
from app.exceptions.ticket import TicketNotFoundError
from app.models.ticket import Ticket
from app.repositories.ticket import TicketRepository
from app.schemas.clients.events import (
    ProviderRegistrationRequest,
    ProviderUnregisterRequest,
)
from app.schemas.ticket import TicketRegisterRequest, TicketRegisterResponse


class TicketService:
    def __init__(
        self,
        repository: TicketRepository,
        provider: EventsProviderClient,
    ):
        self.repository = repository
        self.provider = provider

    async def register(
        self,
        request: TicketRegisterRequest,
    ) -> TicketRegisterResponse:

        provider_request = ProviderRegistrationRequest(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            seat=request.seat,
        )

        provider_response = await self.provider.register(
            event_id=request.event_id,
            registration=provider_request,
        )

        ticket = Ticket(
            ticket_id=provider_response.ticket_id,
            event_id=request.event_id,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            seat=request.seat,
        )

        await self.repository.create(ticket)

        return TicketRegisterResponse(
            ticket_id=provider_response.ticket_id,
        )

    async def unregister(self, ticket_id: UUID) -> None:
        ticket = await self.repository.get_by_ticket_id(ticket_id)

        if ticket is None:
            raise TicketNotFoundError()

        provider_request = ProviderUnregisterRequest(
            ticket_id=ticket.ticket_id,
        )

        await self.provider.unregister(
            event_id=ticket.event_id,
            unregister=provider_request,
        )

        await self.repository.delete(ticket)
