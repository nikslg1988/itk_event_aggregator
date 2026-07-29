from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.event import EventNotFoundError


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
