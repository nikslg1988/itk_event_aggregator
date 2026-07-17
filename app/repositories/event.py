from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event


class EventRepository():
    def __init__(self, session: AsyncSession):
        self.session = session