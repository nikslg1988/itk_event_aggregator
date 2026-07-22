from datetime import datetime
from uuid import UUID

from httpx import AsyncClient

from app.schemas.clients.events import (
    ProviderEventsPage,
    ProviderRegistrationRequest,
    ProviderRegistrationResponse,
    ProviderSeatsResponse,
    ProviderUnregisterRequest,
    ProviderUnregisterResponse,
)


class EventsProviderClient:
    def __init__(self, http_client: AsyncClient, base_url: str, api_key: str):

        self.http_client = http_client
        self.base_url = base_url
        self.api_key = api_key

    async def get_events(self, changed_at: datetime) -> ProviderEventsPage:

        changed_at_str = changed_at.date().isoformat()
        response = await self.http_client.get(
            url=f"{self.base_url}/api/events/",
            params={"changed_at": changed_at_str},
            headers={"X-API-Key": self.api_key},
        )

        response.raise_for_status()

        response_data = response.json()

        return ProviderEventsPage.model_validate(response_data)

    async def get_available_seats(
        self,
        event_id: UUID,
    ) -> ProviderSeatsResponse:

        response = await self.http_client.get(
            url=f"{self.base_url}/api/events/{event_id}/seats/",
            headers={"X-API-Key": self.api_key},
        )

        response.raise_for_status()
        response_data = response.json()
        return ProviderSeatsResponse.model_validate(response_data)

    async def register(
        self, event_id: UUID, registration: ProviderRegistrationRequest
    ) -> ProviderRegistrationResponse:

        response = await self.http_client.post(
            url=f"{self.base_url}/api/events/{event_id}/register/",
            headers={"X-API-Key": self.api_key},
            json=registration.model_dump(),
        )

        response.raise_for_status()

        response_data = response.json()
        return ProviderRegistrationResponse.model_validate(response_data)

    async def unregister(
        self,
        event_id: UUID,
        unregister: ProviderUnregisterRequest,
    ) -> ProviderUnregisterResponse:

        response = await self.http_client.request(
            method="DELETE",
            url=f"{self.base_url}/api/events/{event_id}/unregister/",
            headers={"X-API-Key": self.api_key},
            json=unregister.model_dump(),
        )
        response.raise_for_status()

        response_data = response.json()
        return ProviderUnregisterResponse.model_validate(response_data)
