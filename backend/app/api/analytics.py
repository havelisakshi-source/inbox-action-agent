from fastapi import APIRouter
from sqlalchemy import select, func
from app.api.deps import CurrentUser, DbSession
from app.models.email import Email
from datetime import datetime, timedelta, timezone
from collections import Counter

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats(current_user: CurrentUser, db: DbSession):
    # 1. Base counts
    total_res = await db.execute(select(func.count(Email.id)).where(Email.user_id == current_user.id))
    total = total_res.scalar() or 0

    unread_res = await db.execute(select(func.count(Email.id)).where(Email.user_id == current_user.id, Email.is_read == False))
    unread = unread_res.scalar() or 0

    high_res = await db.execute(select(func.count(Email.id)).where(Email.user_id == current_user.id, Email.priority_label == "high"))
    high_priority = high_res.scalar() or 0

    # 2. Categories breakdown
    cat_res = await db.execute(
        select(Email.category, func.count(Email.id))
        .where(Email.user_id == current_user.id)
        .group_by(Email.category)
    )
    categories = [{"name": cat or "Other", "value": count} for cat, count in cat_res.all()]

    # 3. Timeline (Last 7 Days) - Grouped in Python for DB compatibility
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    date_res = await db.execute(
        select(Email.created_at)
        .where(Email.user_id == current_user.id, Email.created_at >= seven_days_ago)
    )
    
    dates = date_res.scalars().all()
    date_counts = Counter([d.strftime("%Y-%m-%d") for d in dates if d])
    timeline = [{"date": k, "count": v} for k, v in sorted(date_counts.items())]

    return {
        "total_emails": total,
        "unread_emails": unread,
        "high_priority_emails": high_priority,
        "categories": categories,
        "timeline": timeline
    }