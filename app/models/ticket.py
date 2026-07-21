from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.event import Event


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[UUID] = mapped_column(PG_UUID, primary_key=True, default=uuid4)
    ticket_id: Mapped[UUID] = mapped_column(PG_UUID, nullable=False)
    event_id: Mapped[UUID] = mapped_column(
        PG_UUID,
        ForeignKey("events.id"),
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    seat: Mapped[str] = mapped_column(String(10), nullable=False)

    event: Mapped["Event"] = relationship(back_populates="tickets")
