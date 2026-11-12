from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Email(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "emails"
    __table_args__ = (
        UniqueConstraint("user_id", "gmail_message_id", name="uq_emails_user_gmail_id"),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    gmail_message_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    thread_id: Mapped[str | None] = mapped_column(String(128), index=True)
    sender_name: Mapped[str | None] = mapped_column(String(255))
    sender_email: Mapped[str | None] = mapped_column(String(255), index=True)
    recipients: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    subject: Mapped[str | None] = mapped_column(String(1000))
    snippet: Mapped[str | None] = mapped_column(String(500))
    received_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    internal_date: Mapped[int | None] = mapped_column(Integer)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_starred: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_attachment: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    gmail_label_ids: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    category: Mapped[str | None] = mapped_column(String(32), index=True)
    category_confidence: Mapped[float | None] = mapped_column(Float)
    category_reason: Mapped[str | None] = mapped_column(Text)
    priority_score: Mapped[int | None] = mapped_column(Integer, index=True)
    priority_label: Mapped[str | None] = mapped_column(String(16), index=True)
    priority_reasons: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    needs_reply: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)

    summary_short: Mapped[str | None] = mapped_column(Text)
    summary_detailed: Mapped[str | None] = mapped_column(Text)

    content_hash: Mapped[str | None] = mapped_column(String(64))
    analysis_version: Mapped[str | None] = mapped_column(String(16))
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class EmailBody(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "email_bodies"

    email_id: Mapped[str] = mapped_column(
        ForeignKey("emails.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    text_content: Mapped[str | None] = mapped_column(Text)
    html_sanitized: Mapped[str | None] = mapped_column(Text)


class EmailAnalysis(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "email_analysis"

    email_id: Mapped[str] = mapped_column(
        ForeignKey("emails.id", ondelete="CASCADE"), index=True, nullable=False
    )
    model: Mapped[str | None] = mapped_column(String(64))
    prompt_version: Mapped[str | None] = mapped_column(String(16))
    purpose: Mapped[str | None] = mapped_column(Text)
    sender_intent: Mapped[str | None] = mapped_column(Text)
    questions: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    action_items: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    deadlines: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    meeting_details: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    urgency_signals: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float)


class Attachment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "attachments"

    email_id: Mapped[str] = mapped_column(
        ForeignKey("emails.id", ondelete="CASCADE"), index=True, nullable=False
    )
    gmail_attachment_id: Mapped[str] = mapped_column(String(255), nullable=False)
    filename: Mapped[str | None] = mapped_column(String(512))
    mime_type: Mapped[str | None] = mapped_column(String(128))
    size_bytes: Mapped[int | None] = mapped_column(Integer)
    is_safe: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Label(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "labels"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_labels_user_name"),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    gmail_label_id: Mapped[str | None] = mapped_column(String(128))
    color: Mapped[str | None] = mapped_column(String(16))
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class EmailLabel(Base):
    __tablename__ = "email_labels"

    email_id: Mapped[str] = mapped_column(
        ForeignKey("emails.id", ondelete="CASCADE"), primary_key=True
    )
    label_id: Mapped[str] = mapped_column(
        ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True
    )


class Feedback(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "feedback"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    email_id: Mapped[str | None] = mapped_column(
        ForeignKey("emails.id", ondelete="CASCADE"), index=True
    )
    feedback_type: Mapped[str] = mapped_column(String(32), nullable=False)
    previous_value: Mapped[str | None] = mapped_column(String(128))
    new_value: Mapped[str | None] = mapped_column(String(128))
    note: Mapped[str | None] = mapped_column(Text)