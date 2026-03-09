from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.task import Task

from src.database.db import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint


class TaskType(Base):
    __tablename__ = "tasktypes"

    __table_args__ = (UniqueConstraint("user_id", "title"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User", back_populates="types")
    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="type",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
