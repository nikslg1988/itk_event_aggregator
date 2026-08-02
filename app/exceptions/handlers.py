from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.event import (
    EventNotFoundError,
    EventNotPublishedError,
    EventProviderError,
    EventRegistrationClosedError,
)
from app.exceptions.place import PlaceNotFoundError
from app.exceptions.ticket import (
    SeatUnavailableError,
    TicketNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EventNotFoundError)
    async def event_not_found_handler(
        request: Request,
        exc: EventNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(TicketNotFoundError)
    async def ticket_not_found_handler(
        request: Request,
        exc: TicketNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "detail": exc.errors(),
            },
        )

    @app.exception_handler(EventNotPublishedError)
    async def event_not_published(
        request: Request,
        exc: EventNotPublishedError,
    ) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(SeatUnavailableError)
    async def seat_unavailable_handler(
        request: Request,
        exc: SeatUnavailableError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(PlaceNotFoundError)
    async def place_not_found_handler(
        request: Request, exc: PlaceNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(EventRegistrationClosedError)
    async def event_registration_closed_handler(
        request: Request, exc: EventRegistrationClosedError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(EventProviderError)
    async def event_provider_error_handler(
        request: Request, exc: EventProviderError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=502,
            content={
                "detail": str(exc),
            },
        )
