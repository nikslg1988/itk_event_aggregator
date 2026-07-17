from datetime import datetime
from math import ceil

from app.repositories.event import EventRepository
from app.schemas.event import EventListResponse, EventResponse


class EventService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def get_events(
        self,
        date_from: datetime | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> EventListResponse:

        total = await self.repository.count(date_from)
        events = await self.repository.get_all(date_from, page, page_size)
        total_pages = ceil(total / page_size)

        if page > 1:
            previous_page = page - 1
        else:
            previous_page = None

        if page < total_pages:
            next_page = page + 1
        else:
            next_page = None

        responses = [EventResponse.model_validate(event) for event in events]

        return EventListResponse(
            count=total,
            next=next_page,
            previous=previous_page,
            results=responses,
        )
