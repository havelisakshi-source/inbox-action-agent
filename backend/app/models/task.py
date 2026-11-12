from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Task(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "tasks"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    email_id: Mapped[str | None] = mapped_column(ForeignKey("emails.id", ondelete="SET NULL"))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    deadline_source: Mapped[str] = mapped_column(String(16), default="none", nullable=False)
    priority: Mapped[str] = mapped_column(String(16), default="normal", nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="pending", nullable=False, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Followup(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "followups"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    thread_id: Mapped[str | None] = mapped_column(String(128), index=True)
    email_id: Mapped[str | None] = mapped_column(ForeignKey("emails.id", ondelete="SET NULL"))
    status: Mapped[str] = mapped_column(String(32), default="awaiting_reply", nullable=False, index=True)
    suggested_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reply_detected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))