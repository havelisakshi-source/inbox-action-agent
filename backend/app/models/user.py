from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC", nullable=False)

    preferences: Mapped["UserPreference"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class UserPreference(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "user_preferences"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    reply_tone: Mapped[str] = mapped_column(String(32), default="professional", nullable=False)
    signature: Mapped[str | None] = mapped_column(String(2000))
    vip_contacts: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    priority_rules: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    categorization_rules: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    auto_approve_action_types: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    theme: Mapped[str] = mapped_column(String(16), default="system", nullable=False)
    daily_summary_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship(back_populates="preferences")


class RefreshToken(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user_agent: Mapped[str | None] = mapped_column(String(512))
    ip: Mapped[str | None] = mapped_column(String(64))


class OAuthCredential(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "oauth_credentials"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    provider: Mapped[str] = mapped_column(String(32), default="google", nullable=False)
    gmail_address: Mapped[str | None] = mapped_column(String(255))
    encrypted_access_token: Mapped[str] = mapped_column(Text, nullable=False)
    encrypted_refresh_token: Mapped[str | None] = mapped_column(Text)
    token_expiry: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    scopes: Mapped[list] = mapped_column(JSON, default=list, nullable=False)


class GmailSyncState(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "gmail_sync_state"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    last_history_id: Mapped[str | None] = mapped_column(String(64))
    last_full_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_incremental_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sync_status: Mapped[str] = mapped_column(String(32), default="idle", nullable=False)
    last_error: Mapped[str | None] = mapped_column(Text)
    consecutive_failures: Mapped[int] = mapped_column(default=0, nullable=False)