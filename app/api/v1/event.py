from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.event import EventRepository
from app.schemas.event import EventListResponse
from app.services.event import EventService

router = APIRouter(prefix="/api/events", tags=["Events"])


async def get_event_service(
    session: AsyncSession = Depends(get_session),
) -> EventService:
    repository = EventRepository(session)
    service = EventService(repository)
    return service


@router.get("", response_model=EventListResponse)
async def get_events(
    date_from: datetime | None = None,
    page: int = 1,
    page_size: int = 20,
    service: EventService = Depends(get_event_service),
) -> EventListResponse:

    return await service.get_events(
        date_from=date_from,
        page=page,
        page_size=page_size,
    )
