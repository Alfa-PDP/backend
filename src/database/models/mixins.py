import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
        primary_key=True,
    )


class TsMixinCreated:
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        default=datetime.utcnow,
        server_default=func.now(),
        nullable=False,
    )


class TsMixinUpdated:
    __abstract__ = True

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        default=datetime.utcnow,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
