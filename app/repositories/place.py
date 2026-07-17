from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.place import Place


class PlaceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Place]:
        result = await self.session.execute(select(Place))
        return list(result.scalars().all())

    async def get_by_id(self, place_id: UUID) -> Place | None:
        result = await self.session.execute(select(Place).where(Place.id == place_id))

        return result.scalar_one_or_none()

    async def create(self, place: Place) -> Place:
        self.session.add(place)
        await self.session.commit()
        await self.session.refresh(place)
        return place

    async def get_by_name(self, name: str) -> Place | None:
        result = await self.session.execute(select(Place).where(Place.name == name))
        return result.scalar_one_or_none()

    async def delete(self, place: Place) -> None:
        await self.session.delete(place)
        await self.session.commit()
