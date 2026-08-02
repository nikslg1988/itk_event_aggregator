from datetime import datetime, timezone

import httpx

from app.exceptions.event import EventProviderError
from app.models.enums import SyncStatus
from app.models.event import Event
from app.models.place import Place
from app.repositories.event import EventRepository
from app.repositories.place import PlaceRepository
from app.repositories.sync import SyncMetadataRepository
from app.schemas.clients.events import ProviderEvent, ProviderPlace
from app.services.events_paginator import EventsPaginator


class SyncService:
    def __init__(
        self,
        event_repository: EventRepository,
        place_repository: PlaceRepository,
        sync_metadata_repository: SyncMetadataRepository,
        events_paginator: EventsPaginator,
    ):
        self.event_repository = event_repository
        self.place_repository = place_repository
        self.sync_metadata_repository = sync_metadata_repository
        self.events_paginator = events_paginator

    async def synchronize(self) -> None:
        metadata = await self.sync_metadata_repository.get_or_create()

        metadata.sync_status = SyncStatus.RUNNING
        metadata.last_error = None
        await self.sync_metadata_repository.update(metadata)

        try:
            changed_at = metadata.last_changed_at or datetime(
                2000, 1, 1, tzinfo=timezone.utc
            )

            max_changed_at = metadata.last_changed_at
            try:
                async for provider_event in self.events_paginator.iterate(changed_at):
                    await self._process_place(provider_event.place)
                    await self._process_event(provider_event)

                    if (
                        max_changed_at is None
                        or provider_event.changed_at > max_changed_at
                    ):
                        max_changed_at = provider_event.changed_at
            except httpx.HTTPStatusError as exc:
                raise EventProviderError() from exc

            metadata.last_changed_at = max_changed_at
            metadata.last_sync_time = datetime.now(timezone.utc)
            metadata.sync_status = SyncStatus.SUCCESS

        except Exception as exc:
            metadata.sync_status = SyncStatus.FAILED
            metadata.last_error = str(exc)
            raise

        finally:
            await self.sync_metadata_repository.update(metadata)

    async def _process_place(
        self,
        provider_place: ProviderPlace,
    ) -> None:
        place = await self.place_repository.get_by_id(provider_place.id)

        if place is None:
            place = Place(
                id=provider_place.id,
                name=provider_place.name,
                city=provider_place.city,
                address=provider_place.address,
                seats_pattern=provider_place.seats_pattern,
                changed_at=provider_place.changed_at,
                created_at=provider_place.created_at,
            )

            await self.place_repository.create(place)
            return

        place.name = provider_place.name
        place.city = provider_place.city
        place.address = provider_place.address
        place.seats_pattern = provider_place.seats_pattern
        place.changed_at = provider_place.changed_at
        place.created_at = provider_place.created_at

        await self.place_repository.update(place)

    async def _process_event(
        self,
        provider_event: ProviderEvent,
    ) -> None:
        event = await self.event_repository.get_by_id(provider_event.id)

        if event is None:
            event = Event(
                id=provider_event.id,
                place_id=provider_event.place.id,
                name=provider_event.name,
                event_time=provider_event.event_time,
                registration_deadline=provider_event.registration_deadline,
                status=provider_event.status,
                number_of_visitors=provider_event.number_of_visitors,
                changed_at=provider_event.changed_at,
                created_at=provider_event.created_at,
                status_changed_at=provider_event.status_changed_at,
            )

            await self.event_repository.create(event)
            return

        event.place_id = provider_event.place.id
        event.name = provider_event.name
        event.event_time = provider_event.event_time
        event.registration_deadline = provider_event.registration_deadline
        event.status = provider_event.status
        event.number_of_visitors = provider_event.number_of_visitors
        event.changed_at = provider_event.changed_at
        event.created_at = provider_event.created_at
        event.status_changed_at = provider_event.status_changed_at

        await self.event_repository.update(event)
