from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from app.schemas.clients.events import ProviderSeatsResponse


@dataclass
class CacheEntry:
    response: ProviderSeatsResponse
    expires_at: datetime


class SeatCache:
    def __init__(self, ttl_seconds: int = 30):
        self._cache: dict[UUID, CacheEntry] = {}
        self._ttl_seconds = ttl_seconds

    def get(self, event_id: UUID) -> ProviderSeatsResponse | None:
        entry = self._cache.get(event_id)
        if entry is None:
            return None

        if datetime.now() >= entry.expires_at:
            del self._cache[event_id]
            return None

        return entry.response

    def set(self, event_id: UUID, response: ProviderSeatsResponse) -> None:
        expires_at = datetime.now() + timedelta(seconds=self._ttl_seconds)

        self._cache[event_id] = CacheEntry(response=response, expires_at=expires_at)
