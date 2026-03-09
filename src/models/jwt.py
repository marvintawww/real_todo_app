from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime, timezone

from src.database.db import Base


class JWTBlacklist(Base):
    __tablename__ = "jwt_blacklist"

    id: Mapped[int] = mapped_column(primary_key=True)
    jti: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
