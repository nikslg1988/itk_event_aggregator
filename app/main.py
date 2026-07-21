from fastapi import FastAPI

from app.api.v1.event import router as event_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(event_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
