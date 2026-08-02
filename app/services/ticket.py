from datetime import UTC, datetime
from uuid import UUID

import httpx

from app.cache.seat_cache import SeatCache
from app.clients.events import EventsProviderClient
from app.exceptions.event import (
    EventNotFoundError,
    EventNotPublishedError,
    EventProviderError,
    EventRegistrationClosedError,
)
from app.exceptions.ticket import SeatUnavailableError, TicketNotFoundError
from app.models.enums import EventStatus
from app.models.ticket import Ticket
from app.repositories.event import EventRepository
from app.repositories.ticket import TicketRepository
from app.schemas.clients.events import (
    ProviderRegistrationRequest,
    ProviderUnregisterRequest,
)
from app.schemas.ticket import AvailableSeatsResponse, TicketRegisterRequest


class TicketService:
    def __init__(
        self,
        ticket_repository: TicketRepository,
        event_repository: EventRepository,
        provider: EventsProviderClient,
        seat_cache: SeatCache,
    ):

        self.ticket_repository = ticket_repository
        self.event_repository = event_repository
        self.provider = provider
        self.seat_cache = seat_cache

    async def register(
        self,
        request: TicketRegisterRequest,
    ) -> UUID:
        event_id = request.event_id
        event = await self.event_repository.get_by_id(event_id)

        if event is None:
            raise EventNotFoundError()

        if event.status != EventStatus.PUBLISHED:
            raise EventNotPublishedError()

        now = datetime.now(UTC)

        if now > event.registration_deadline:
            raise EventRegistrationClosedError()

        available_seats = await self.provider.get_available_seats(event_id)

        if request.seat not in available_seats.seats:
            raise SeatUnavailableError(request.seat)

        provider_request = ProviderRegistrationRequest(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            seat=request.seat,
        )

        try:
            provider_response = await self.provider.register(
                event_id=event_id,
                registration=provider_request,
            )
        except httpx.HTTPStatusError as exc:
            raise EventProviderError() from exc

        ticket = Ticket(
            ticket_id=provider_response.ticket_id,
            event_id=event_id,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            seat=request.seat,
        )

        await self.ticket_repository.create(ticket)

        return provider_response.ticket_id

    async def unregister(self, ticket_id: UUID) -> None:
        ticket = await self.ticket_repository.get_by_ticket_id(ticket_id)

        if ticket is None:
            raise TicketNotFoundError("Ticket Not Found")

        provider_request = ProviderUnregisterRequest(
            ticket_id=ticket.ticket_id,
        )
        try:
            await self.provider.unregister(
                event_id=ticket.event_id,
                unregister=provider_request,
            )
        except httpx.HTTPStatusError as exc:
            raise EventProviderError() from exc

        await self.ticket_repository.delete(ticket)

    async def get_available_seats(
        self,
        event_id: UUID,
    ) -> AvailableSeatsResponse:

        event = await self.event_repository.get_by_id(event_id)

        if event is None:
            raise EventNotFoundError()

        if event.status != EventStatus.PUBLISHED:
            raise EventNotPublishedError()

        response = self.seat_cache.get(event_id)

        if response is None:
            try:
                response = await self.provider.get_available_seats(event_id)
            except httpx.HTTPStatusError as exc:
                raise EventProviderError() from exc
            self.seat_cache.set(event_id, response)

        return AvailableSeatsResponse(
            event_id=event_id,
            available_seats=response.seats,
        )
