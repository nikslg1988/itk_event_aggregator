from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event


class EventRepository:
    def __init__(self, session: AsyncSession):

        self.session = session

    async def get_by_id(self, event_id: UUID) -> Event | None:
        result = await self.session.execute(select(Event).where(Event.id == event_id))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        date_from: datetime | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[Event]:

        query = select(Event)

        if date_from is not None:
            query = query.where(Event.event_time >= date_from)

        query = query.order_by(Event.event_time)
        query = query.offset((page - 1) * page_size)
        query = query.limit(page_size)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count(self, date_from: datetime | None = None) -> int:

        query = select(func.count(Event.id))

        if date_from is not None:
            query = query.where(Event.event_time >= date_from)

        result = await self.session.execute(query)
        return result.scalar_one()
