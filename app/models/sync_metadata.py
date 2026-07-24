from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Enum, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import SyncStatus


class SyncMetadata(Base):
    __tablename__ = "sync_metadata"

    id: Mapped[UUID] = mapped_column(
        PG_UUID,
        primary_key=True,
        default=uuid4,
    )

    last_sync_time: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    last_changed_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    sync_status: Mapped[SyncStatus] = mapped_column(
        Enum(SyncStatus),
        nullable=False,
        default=SyncStatus.PENDING,
    )

    last_error: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
