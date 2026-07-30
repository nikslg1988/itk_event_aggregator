from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import AsyncClient

from app.api.v1.event import router as event_router
from app.api.v1.sync import router as sync_router
from app.api.v1.tickets import router as ticket_router
from app.clients.events import EventsProviderClient
from app.core.setting import EVENTS_PROVIDER_API_KEY, EVENTS_PROVIDER_BASE_URL
from app.db.session import session_factory
from app.exceptions.handlers import register_exception_handlers
from app.repositories.event import EventRepository
from app.repositories.place import PlaceRepository
from app.repositories.sync import SyncMetadataRepository
from app.services.events_paginator import EventsPaginator
from app.services.sync import SyncService
from app.workers.sync import SyncWorker


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with AsyncClient(follow_redirects=True) as client:
        events_provider = EventsProviderClient(
            http_client=client,
            base_url=EVENTS_PROVIDER_BASE_URL,
            api_key=EVENTS_PROVIDER_API_KEY,
        )

        events_paginator = EventsPaginator(events_provider)

        async with session_factory() as session:
            event_repository = EventRepository(session)
            place_repository = PlaceRepository(session)
            sync_metadata_repository = SyncMetadataRepository(session)

            sync_service = SyncService(
                event_repository=event_repository,
                place_repository=place_repository,
                sync_metadata_repository=sync_metadata_repository,
                events_paginator=events_paginator,
            )

            worker = SyncWorker(sync_service)
            await worker.start()

            try:
                yield
            finally:
                await worker.stop()


app = FastAPI(
    title="itk_event_agreggator",
    version="0.1.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(event_router)
app.include_router(ticket_router)
app.include_router(sync_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
