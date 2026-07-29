from datetime import datetime
from typing import AsyncIterator

from app.clients.events import EventsProviderClient
from app.schemas.clients.events import ProviderEvent


class EventsPaginator:
    def __init__(
        self,
        events_provider_client: EventsProviderClient,
    ):
        self.events_provider_client = events_provider_client

    async def iterate(
        self,
        changed_at: datetime,
    ) -> AsyncIterator[ProviderEvent]:

        page = await self.events_provider_client.get_changed_events(changed_at)

        while True:
            for result in page.results:
                yield result

            if page.next is None:
                break

            page = await self.events_provider_client.get_events_page(page.next)
