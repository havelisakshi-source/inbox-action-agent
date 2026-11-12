from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Action(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "actions"
    __table_args__ = (
        UniqueConstraint("idempotency_key", name="uq_actions_idempotency_key"),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    run_id: Mapped[str | None] = mapped_column(ForeignKey("agent_runs.id", ondelete="SET NULL"))
    email_id: Mapped[str | None] = mapped_column(ForeignKey("emails.id", ondelete="SET NULL"))
    thread_id: Mapped[str | None] = mapped_column(String(128))
    action_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    expected_outcome: Mapped[str | None] = mapped_column(Text)
    risk_level: Mapped[str] = mapped_column(String(16), default="moderate", nullable=False)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="proposed", nullable=False, index=True)
    idempotency_key: Mapped[str] = mapped_column(String(64), nullable=False)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    executed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    execution_result: Mapped[dict | None] = mapped_column(JSON)
    verification_result: Mapped[dict | None] = mapped_column(JSON)
    error: Mapped[str | None] = mapped_column(Text)


class ActionHistory(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "action_history"

    action_id: Mapped[str] = mapped_column(
        ForeignKey("actions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    event: Mapped[str] = mapped_column(String(64), nullable=False)
    details: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class Draft(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "drafts"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    email_id: Mapped[str | None] = mapped_column(ForeignKey("emails.id", ondelete="SET NULL"))
    thread_id: Mapped[str | None] = mapped_column(String(128))
    gmail_draft_id: Mapped[str | None] = mapped_column(String(128))
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    tone: Mapped[str | None] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(16), default="local", nullable=False)