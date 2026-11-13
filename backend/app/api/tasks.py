from fastapi import APIRouter
from sqlalchemy import select
from app.api.deps import CurrentUser, DbSession
from app.models.task import Task

router = APIRouter()

@router.get("")
async def list_tasks(current_user: CurrentUser, db: DbSession):
    res = await db.execute(
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
    )
    tasks = res.scalars().all()
    return [
        {
            "id": t.id,
            "description": t.description,
            "status": t.status,
            "deadline": t.deadline,
            "priority": t.priority
        } for t in tasks
    ]