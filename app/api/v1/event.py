from datetime import datetime

from fastapi import APIRouter, Depends

from app.dependencies.dependencies import get_event_service
from app.schemas.event import EventListResponse
from app.services.event import EventService

router = APIRouter(prefix="/api/events", tags=["Events"])


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
