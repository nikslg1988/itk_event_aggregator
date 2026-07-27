from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sync_metadata import SyncMetadata


class SyncMetadataRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self) -> SyncMetadata:
        result = await self.session.execute(select(SyncMetadata))
        metadata = result.scalar_one_or_none()

        if metadata is None:
            metadata = SyncMetadata()
            self.session.add(metadata)
            await self.session.commit()
            await self.session.refresh(metadata)
        return metadata

    async def update(self, metadata: SyncMetadata) -> SyncMetadata:
        await self.session.commit()
        return metadata
