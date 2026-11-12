from sqlalchemy import JSON, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class AgentMemory(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "agent_memory"
    __table_args__ = (
        UniqueConstraint("user_id", "memory_type", "key", name="uq_memory_user_type_key"),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    memory_type: Mapped[str] = mapped_column(String(32), nullable=False)
    key: Mapped[str] = mapped_column(String(128), nullable=False)
    value: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    source: Mapped[str] = mapped_column(String(32), default="user_explicit", nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float)