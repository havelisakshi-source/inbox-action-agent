from fastapi import APIRouter
from sqlalchemy import select, func
from app.api.deps import CurrentUser, DbSession
from app.models.email import Email
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats(current_user: CurrentUser, db: DbSession):
    total_res = await db.execute(select(func.count(Email.id)).where(Email.user_id == current_user.id))
    total = total_res.scalar() or 0

    unread_res = await db.execute(select(func.count(Email.id)).where(Email.user_id == current_user.id, Email.is_read == False))
    unread = unread_res.scalar() or 0

    high_res = await db.execute(select(func.count(Email.id)).where(Email.user_id == current_user.id, Email.priority_label == "high"))
    high_priority = high_res.scalar() or 0

    cat_res = await db.execute(
        select(Email.category, func.count(Email.id))
        .where(Email.user_id == current_user.id)
        .group_by(Email.category)
    )
    categories = [{"name": cat or "Other", "value": count} for cat, count in cat_res.all()]

    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    date_res = await db.execute(
        select(func.date(Email.created_at), func.count(Email.id))
        .where(Email.user_id == current_user.id, Email.created_at >= seven_days_ago)
        .group_by(func.date(Email.created_at))
        .order_by(func.date(Email.created_at))
    )
    timeline = [{"date": str(d), "count": c} for d, c in date_res.all()]

    return {
        "total_emails": total,
        "unread_emails": unread,
        "high_priority_emails": high_priority,
        "categories": categories,
        "timeline": timeline
    }