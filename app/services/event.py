from datetime import date
from math import ceil
from uuid import UUID

from app.exceptions.event import EventNotFoundError
from app.repositories.event import EventRepository
from app.schemas.event import EventListResult, EventResponse


class EventService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def get_events(
        self,
        date_from: date | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> EventListResult:

        total = await self.repository.count(date_from)
        events = await self.repository.get_all(date_from, page, page_size)
        total_pages = max(1, ceil(total / page_size))

        if page > 1:
            previous_page = page - 1
        else:
            previous_page = None

        if page < total_pages:
            next_page = page + 1
        else:
            next_page = None

        responses = [EventResponse.model_validate(event) for event in events]

        return EventListResult(
            count=total,
            next=next_page,
            previous=previous_page,
            results=responses,
        )

    async def get_event_by_id(self, event_id: UUID) -> EventResponse:
        event = await self.repository.get_by_id(event_id)

        if event is None:
            raise EventNotFoundError("Event Not Found")

        return EventResponse.model_validate(event)
