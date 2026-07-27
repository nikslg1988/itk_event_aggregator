from fastapi import APIRouter, Depends

from app.dependencies.dependencies import get_sync_service
from app.services.sync import SyncService

router = APIRouter(
    prefix="/api/sync",
    tags=["Synchronization"],
)


@router.post("/trigger")
async def trigger_sync(service: SyncService = Depends(get_sync_service)):
    await service.synchronize()
    return {"status": "Synchronization"}
