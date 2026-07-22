from collections.abc import AsyncGenerator

from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.events import EventsProviderClient
from app.core.setting import EVENTS_PROVIDER_API_KEY, EVENTS_PROVIDER_BASE_URL
from app.db.session import get_session
from app.repositories.event import EventRepository
from app.repositories.ticket import TicketRepository
from app.services.event import EventService
from app.services.ticket import TicketService


async def get_http_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient() as client:
        yield client


async def get_events_provider(
    http_client: AsyncClient = Depends(get_http_client),
) -> EventsProviderClient:

    if EVENTS_PROVIDER_API_KEY is None:
        raise RuntimeError("EVENTS_PROVIDER_API_KEY is not configured")

    if EVENTS_PROVIDER_BASE_URL is None:
        raise RuntimeError("EVENTS_PROVIDER_BASE_URL is not configured")

    return EventsProviderClient(
        http_client=http_client,
        base_url=EVENTS_PROVIDER_BASE_URL,
        api_key=EVENTS_PROVIDER_API_KEY,
    )


async def get_event_service(
    session: AsyncSession = Depends(get_session),
) -> EventService:
    repository = EventRepository(session)
    service = EventService(repository)
    return service


def get_ticket_service(
    session: AsyncSession = Depends(get_session),
    repository: EventRepository = Depends(),
    provider: EventsProviderClient = Depends(get_events_provider),
) -> TicketService:
    ticket_repository = TicketRepository(session)
    return TicketService(ticket_repository, repository, provider)
