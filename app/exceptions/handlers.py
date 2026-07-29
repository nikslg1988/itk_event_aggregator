from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.event import EventNotFoundError
from app.exceptions.ticket import TicketNotFoundError


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
