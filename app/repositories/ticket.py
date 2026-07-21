from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket


class TicketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket

    async def get_by_ticket_id(self, ticket_id: UUID) -> Ticket | None:
        result = await self.session.execute(
            select(Ticket).where(Ticket.ticket_id == ticket_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, ticket: Ticket) -> None:
        await self.session.delete(ticket)
        await self.session.commit()
