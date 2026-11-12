from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog


class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log(
        self,
        *,
        operation: str,
        user_id: str | None = None,
        actor: str = "system",
        resource_type: str | None = None,
        resource_id: str | None = None,
        ip: str | None = None,
        user_agent: str | None = None,
        outcome: str = "success",
    ) -> None:
        entry = AuditLog(
            user_id=user_id,
            actor=actor,
            operation=operation,
            resource_type=resource_type,
            resource_id=resource_id,
            ip=ip,
            user_agent=user_agent,
            outcome=outcome,
        )
        self.db.add(entry)
        await self.db.flush()