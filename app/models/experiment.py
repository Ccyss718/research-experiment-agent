from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from enum import Enum
from sqlalchemy import Enum as SQLEnum
from app.db.base import Base

from datetime import datetime

class ExperimentStatus(str, Enum):
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    FAILED = "failed"


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(
        Text,
        default=None,
        nullable=True

    )

    hypothesis: Mapped[str | None] = mapped_column(
        Text,
        default=None,
        nullable=True
    )

    status: Mapped[ExperimentStatus] = mapped_column(
        SQLEnum(
            ExperimentStatus,
            name="experiment_status",
            values_callable=lambda enum_cls: [
                status.value for status in enum_cls
            ],
        ),
        default=ExperimentStatus.PLANNED,
        server_default=ExperimentStatus.PLANNED.value,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


