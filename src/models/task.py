from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.type import TaskType

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, UniqueConstraint, Date
from datetime import datetime, timezone, date

from src.database.db import Base


class Task(Base):
    __tablename__ = "tasks"

    __table_args__ = (UniqueConstraint("user_id", "title"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    task_date: Mapped[date] = mapped_column(Date, default=lambda: date.today())
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    type_id: Mapped[int] = mapped_column(ForeignKey("tasktypes.id", ondelete="CASCADE"))
    type: Mapped["TaskType"] = relationship("TaskType", back_populates="tasks")
