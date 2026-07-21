from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.place import Place
    from app.models.ticket import Ticket


class Event(Base):
    __tablename__ = "events"

    id: Mapped[UUID] = mapped_column(PG_UUID, primary_key=True, default=uuid4)
    place_id: Mapped[UUID] = mapped_column(
        PG_UUID, ForeignKey("places.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    event_time: Mapped[datetime] = mapped_column(nullable=False)
    registration_deadline: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    number_of_visitors: Mapped[int] = mapped_column(Integer, nullable=False)
    changed_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    status_changed_at: Mapped[datetime] = mapped_column(nullable=False)

    place: Mapped["Place"] = relationship(back_populates="events")
    ticket: Mapped["Ticket"] = relationship(back_populates="events")
