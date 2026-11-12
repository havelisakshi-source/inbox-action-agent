from fastapi import APIRouter
from sqlalchemy import text

from app.api.deps import DbSession

router = APIRouter()


@router.get("/health")
async def health(db: DbSession) -> dict:
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "reachable"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "degraded", "database": "unreachable", "error": str(exc)}


@router.get("/version")
async def version() -> dict:
    return {"name": "Inbox Action Agent", "version": "0.1.0"}