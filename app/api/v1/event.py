from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request

from app.dependencies.dependencies import get_event_service
from app.schemas.event import EventListResponse, EventResponse
from app.services.event import EventService

router = APIRouter(prefix="/api/events", tags=["Events"])


@router.get("", response_model=EventListResponse)
async def get_events(
    request: Request,
    date_from: date | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    service: EventService = Depends(get_event_service),
) -> EventListResponse:

    result = await service.get_events(
        date_from=date_from,
        page=page,
        page_size=page_size,
    )

    next_url = None
    if result.next is not None:
        next_url = str(request.url.include_query_params(page=result.next))

    previous_url = None
    if result.previous is not None:
        previous_url = str(request.url.include_query_params(page=result.previous))

    return EventListResponse(
        count=result.count,
        next=next_url,
        previous=previous_url,
        results=result.results,
    )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event_by_id(
    event_id: UUID, service: EventService = Depends(get_event_service)
) -> EventResponse:
    result = await service.get_event_by_id(event_id)

    return result
