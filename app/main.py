from fastapi import FastAPI

from app.api.v1.event import router as event_router
from app.api.v1.sync import router as sync_router
from app.api.v1.tickets import router as ticket_router
from app.exceptions.handlers import register_exception_handlers

app = FastAPI(title="itk_event_agreggator", version="0.1.0")

register_exception_handlers(app)

app.include_router(event_router)
app.include_router(ticket_router)
app.include_router(sync_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
