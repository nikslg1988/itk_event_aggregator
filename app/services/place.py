from uuid import UUID

from app.models.place import Place
from app.repositories.place import PlaceRepository
from app.exceptions.place import PlaceAlreadyExistsError, PlaceNotFoundError


class PlaceService:
    def __init__(self, repository: PlaceRepository):
        self.repository = repository

    async def get_all(self) -> list[Place]:
        return await self.repository.get_all()

    async def get_by_id(self, place_id: UUID) -> Place:
        existing = await self.repository.get_by_id(place_id)
        if existing is None:
            raise PlaceNotFoundError()

        return existing

    async def create(self, place: Place) -> Place:
        existing = await self.repository.get_by_name(place.name)
        if existing is not None:
            raise PlaceAlreadyExistsError()

        return await self.repository.create(place)

    async def delete(self, place_id: UUID) -> None:
        existing = await self.repository.get_by_id(place_id)
        if existing is None:
            raise PlaceNotFoundError()
        await self.repository.delete(existing)
