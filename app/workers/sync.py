import asyncio
import logging

from app.services.sync import SyncService

logger = logging.getLogger(__name__)


class SyncWorker:
    def __init__(
        self,
        sync_service: SyncService,
        interval_seconds: int = 86400,
    ):
        self._sync_service = sync_service
        self._interval_seconds = interval_seconds
        self._task: asyncio.Task[None] | None = None

    async def start(self):
        if self._task is not None:
            return
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        if self._task is not None:
            try:
                self._task.cancel()
                await self._task
            except asyncio.CancelledError:
                pass
            finally:
                self._task = None

    async def _run(self):
        while True:
            logger.info("Background synchronization started")
            try:
                await self._sync_service.synchronize()
                logger.info("Background synchronization finished")
            except Exception:
                logger.exception("Background synchronization failed")
            await asyncio.sleep(self._interval_seconds)
