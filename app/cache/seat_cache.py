from dataclasses import dataclass
from datetime import datetime

from app.schemas.clients.events import ProviderSeatsResponse


@dataclass
class CacheEntry:
    response: ProviderSeatsResponse
    expires_at: datetime


class SeatCache:
    def __init__(
        self,
    ):
        pass

    def set(self):
        pass

    def get(self):
        pass
