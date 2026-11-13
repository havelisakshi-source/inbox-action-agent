from fastapi import APIRouter
from sqlalchemy import select
from app.api.deps import CurrentUser, DbSession
from app.models.action import ActionHistory

router = APIRouter()

@router.get("")
async def get_history(current_user: CurrentUser, db: DbSession):
    res = await db.execute(
        select(ActionHistory)
        .where(ActionHistory.user_id == current_user.id)
        .order_by(ActionHistory.created_at.desc())
        .limit(50)
    )
    history = res.scalars().all()
    
    return [
        {
            "id": h.id,
            "event": h.event,
            "details": h.details,
            "created_at": h.created_at
        } for h in history
    ]