from datetime import datetime
from uuid import uuid4

import httpx
import pytest


@pytest.mark.asyncio
async def test_get_changed_events(
    client,
    http_client,
    response,
    provider_events_page,
):
    # Arrange
    changed_at = datetime(2026, 7, 31)

    response.json.return_value = provider_events_page.model_dump(mode="json")
    http_client.get.return_value = response
    # Act
    result = await client.get_changed_events(changed_at)
    # Assert
    http_client.get.assert_awaited_once_with(
        url="https://test.api/api/events/",
        params={"changed_at": changed_at.date().isoformat()},
        headers={"X-API-Key": "test_api_key"},
    )

    assert result == provider_events_page


@pytest.mark.asyncio
async def test_get_events_page(response, http_client, provider_events_page, client):
    # Arrange
    response.json.return_value = provider_events_page.model_dump(mode="json")
    http_client.get.return_value = response

    url = "https://test.api/api/events/?page=2"

    # Act
    result = await client.get_events_page(url)
    # Assert
    http_client.get.assert_awaited_once_with(
        url=url,
        headers={
            "X-API-Key": "test_api_key",
        },
    )
    assert result == provider_events_page


@pytest.mark.asyncio
async def test_get_available_seats(
    response, http_client, provider_seats_response, client
):
    # Arrange
    response.json.return_value = provider_seats_response.model_dump(mode="json")
    http_client.get.return_value = response

    event_id = uuid4()

    # Act
    result = await client.get_available_seats(event_id)

    # Assert
    http_client.get.assert_awaited_once_with(
        url=f"https://test.api/api/events/{event_id}/seats/",
        headers={"X-API-Key": "test_api_key"},
    )
    assert result == provider_seats_response


@pytest.mark.asyncio
async def test_register(
    client,
    http_client,
    response,
    provider_registration_response,
    provider_registration_request,
):
    # Arrange
    response.json.return_value = provider_registration_response.model_dump(mode="json")
    http_client.post.return_value = response
    event_id = uuid4()
    # Act
    result = await client.register(event_id, provider_registration_request)
    # Assert
    http_client.post.assert_awaited_once_with(
        url=f"https://test.api/api/events/{event_id}/register/",
        headers={"X-API-Key": "test_api_key"},
        json=provider_registration_request.model_dump(mode="json"),
    )

    assert result == provider_registration_response


@pytest.mark.asyncio
async def test_unregister(
    client,
    http_client,
    response,
    provider_unregister_request,
    provider_unregister_response,
):
    # Arrange
    response.json.return_value = provider_unregister_response.model_dump(mode="json")
    http_client.request.return_value = response

    event_id = uuid4()

    # Act
    result = await client.unregister(
        event_id,
        provider_unregister_request,
    )

    # Assert
    http_client.request.assert_awaited_once_with(
        method="DELETE",
        url=f"https://test.api/api/events/{event_id}/unregister/",
        headers={
            "X-API-Key": "test_api_key",
        },
        json=provider_unregister_request.model_dump(mode="json"),
    )

    assert result == provider_unregister_response


@pytest.mark.asyncio
async def test_get_available_seats_http_error(
    client,
    http_client,
    response,
):
    # Arrange
    event_id = uuid4()
    request = httpx.Request("GET", f"https://test.api/api/events/{event_id}/seats/")
    http_response = httpx.Response(status_code=500, request=request)
    response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Internal Server Error",
        request=request,
        response=http_response,
    )
    http_client.get.return_value = response

    # Act / Assert
    with pytest.raises(httpx.HTTPStatusError):
        await client.get_available_seats(event_id)

    http_client.get.assert_awaited_once_with(
        url=f"https://test.api/api/events/{event_id}/seats/",
        headers={"X-API-Key": "test_api_key"},
    )
    response.raise_for_status.assert_called_once_with()


@pytest.mark.asyncio
async def test_register_http_error(
    client,
    http_client,
    response,
    provider_registration_request,
):
    # Arrange
    event_id = uuid4()

    request = httpx.Request(
        "POST",
        f"https://test.api/api/events/{event_id}/register/",
    )

    http_response = httpx.Response(
        status_code=500,
        request=request,
    )

    response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Internal Server Error",
        request=request,
        response=http_response,
    )

    http_client.post.return_value = response

    # Act / Assert
    with pytest.raises(httpx.HTTPStatusError):
        await client.register(
            event_id,
            provider_registration_request,
        )

    http_client.post.assert_awaited_once_with(
        url=f"https://test.api/api/events/{event_id}/register/",
        headers={"X-API-Key": "test_api_key"},
        json=provider_registration_request.model_dump(mode="json"),
    )

    response.raise_for_status.assert_called_once_with()


@pytest.mark.asyncio
async def test_unregister_http_error(
    client,
    http_client,
    response,
    provider_unregistration_request,
):
    # Arrange
    event_id = uuid4()

    request = httpx.Request(
        "DELETE",
        f"https://test.api/api/events/{event_id}/unregister/",
    )

    http_response = httpx.Response(
        status_code=500,
        request=request,
    )

    response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Internal Server Error",
        request=request,
        response=http_response,
    )

    http_client.request.return_value = response

    # Act / Assert
    with pytest.raises(httpx.HTTPStatusError):
        await client.unregister(
            event_id,
            provider_unregistration_request,
        )

    http_client.request.assert_awaited_once_with(
        method="DELETE",
        url=f"https://test.api/api/events/{event_id}/unregister/",
        headers={"X-API-Key": "test_api_key"},
        json=provider_unregistration_request.model_dump(mode="json"),
    )

    response.raise_for_status.assert_called_once_with()
