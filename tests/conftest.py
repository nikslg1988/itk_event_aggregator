from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.clients.events import EventsProviderClient
from app.models.enums import EventStatus
from app.schemas.clients.events import (
    ProviderEvent,
    ProviderEventsPage,
    ProviderPlace,
    ProviderRegistrationRequest,
    ProviderRegistrationResponse,
    ProviderSeatsResponse,
    ProviderUnregisterRequest,
    ProviderUnregisterResponse,
)


@pytest.fixture
def http_client():
    return AsyncMock()


@pytest.fixture
def response():
    return MagicMock()


@pytest.fixture
def client(http_client):
    return EventsProviderClient(
        http_client=http_client,
        base_url="https://test.api",
        api_key="test_api_key",
    )


@pytest.fixture
def now():
    return datetime(2026, 7, 31)


@pytest.fixture
def provider_place(now):
    return ProviderPlace(
        id=uuid4(),
        name="Test Place",
        city="Москва",
        address="ул. Пушкина",
        seats_pattern="A1-100",
        changed_at=now,
        created_at=now,
    )


@pytest.fixture
def provider_event(provider_place, now):
    return ProviderEvent(
        id=uuid4(),
        name="Test Event",
        place=provider_place,
        event_time=now,
        registration_deadline=now,
        status=EventStatus.PUBLISHED,  # TODO
        number_of_visitors=100,
        changed_at=now,
        created_at=now,
        status_changed_at=now,
    )


@pytest.fixture
def provider_events_page(provider_event):
    return ProviderEventsPage(
        next=None,
        previous=None,
        results=[provider_event],
    )


@pytest.fixture
def provider_seats_response():
    return ProviderSeatsResponse(
        seats=[
            "A1",
            "A2",
            "B5",
        ]
    )


@pytest.fixture
def provider_registration_response():
    return ProviderRegistrationResponse(
        ticket_id=uuid4(),
    )


@pytest.fixture
def provider_registration_request():
    return ProviderRegistrationRequest(
        first_name="Иван",
        last_name="Иванов",
        seat="A1",
        email="ivan@example.com",
    )


@pytest.fixture
def provider_unregister_request():
    return ProviderUnregisterRequest(
        ticket_id=uuid4(),
    )


@pytest.fixture
def provider_unregister_response():
    return ProviderUnregisterResponse(
        success=True,
    )


@pytest.fixture
def events_provider_client():
    return AsyncMock(spec=EventsProviderClient)


@pytest.fixture
def provider_unregistration_request() -> ProviderUnregisterRequest:
    return ProviderUnregisterRequest(
        ticket_id=uuid4(),
    )
