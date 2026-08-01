from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.clients.events import EventsProviderClient
from app.schemas.clients.events import ProviderEvent, ProviderEventsPage, ProviderPlace
from app.services.events_paginator import EventsPaginator


@pytest.mark.asyncio
async def test_iterate_single_page(
    provider_events_page,
):
    # Arrange
    events_provider_client = AsyncMock(spec=EventsProviderClient)
    paginator = EventsPaginator(events_provider_client)
    changed_at = datetime(2026, 7, 31)

    events_provider_client.get_changed_events.return_value = provider_events_page

    # Act
    result = []

    async for event in paginator.iterate(changed_at):
        result.append(event)

    # Assert
    events_provider_client.get_changed_events.assert_awaited_once_with(changed_at)
    events_provider_client.get_events_page.assert_not_awaited()
    assert result == provider_events_page.results


@pytest.mark.asyncio
async def test_iterate_multiple_pages():
    # Arrange
    events_provider_client = AsyncMock(spec=EventsProviderClient)
    paginator = EventsPaginator(events_provider_client)
    changed_at = datetime(2026, 7, 31)
    now = datetime(2026, 8, 1)

    place = ProviderPlace(
        id=uuid4(),
        name="Test Place",
        city="Москва",
        address="ул. Пушкина",
        seats_pattern="A1-100",
        changed_at=now,
        created_at=now,
    )

    event_1 = ProviderEvent(
        id=uuid4(),
        name="Event 1",
        place=place,
        event_time=now,
        registration_deadline=now,
        status="PUBLISHED",
        number_of_visitors=100,
        changed_at=now,
        created_at=now,
        status_changed_at=now,
    )

    event_2 = ProviderEvent(
        id=uuid4(),
        name="Event 2",
        place=place,
        event_time=now,
        registration_deadline=now,
        status="PUBLISHED",
        number_of_visitors=100,
        changed_at=now,
        created_at=now,
        status_changed_at=now,
    )

    event_3 = ProviderEvent(
        id=uuid4(),
        name="Event 3",
        place=place,
        event_time=now,
        registration_deadline=now,
        status="PUBLISHED",
        number_of_visitors=100,
        changed_at=now,
        created_at=now,
        status_changed_at=now,
    )

    page_1 = ProviderEventsPage(
        next="page2",
        previous=None,
        results=[
            event_1,
            event_2,
        ],
    )

    page_2 = ProviderEventsPage(
        next=None,
        previous=None,
        results=[
            event_3,
        ],
    )

    events_provider_client.get_changed_events.return_value = page_1
    events_provider_client.get_events_page.return_value = page_2
    # Act
    result = []

    async for event in paginator.iterate(changed_at):
        result.append(event)

    # Assert
    events_provider_client.get_changed_events.assert_awaited_once_with(changed_at)

    events_provider_client.get_events_page.assert_awaited_once_with("page2")

    assert result == [
        event_1,
        event_2,
        event_3,
    ]


@pytest.mark.asyncio
async def test_iterate_empty_page():
    # Arrange
    events_provider_client = AsyncMock(spec=EventsProviderClient)
    paginator = EventsPaginator(events_provider_client)
    changed_at = datetime(2026, 7, 31)

    empty_page = ProviderEventsPage(
        next=None,
        previous=None,
        results=[],
    )

    events_provider_client.get_changed_events.return_value = empty_page

    # Act
    result = []

    async for event in paginator.iterate(changed_at):
        result.append(event)

    # Assert
    events_provider_client.get_changed_events.assert_awaited_once_with(changed_at)

    events_provider_client.get_events_page.assert_not_awaited()

    assert result == []
