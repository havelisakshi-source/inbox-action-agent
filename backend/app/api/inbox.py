from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.api.deps import CurrentUser, DbSession
from app.models.email import Email
from app.services.gmail_sync_service import GmailSyncService
from app.services.ai_service import AIService
from app.schemas.email import EmailResponse

router = APIRouter()

@router.get("", response_model=list[EmailResponse])
async def list_emails(
    current_user: CurrentUser, 
    db: DbSession, 
    limit: int = 50,
    is_read: bool | None = None,
    priority: str | None = None
):
    query = select(Email).where(Email.user_id == current_user.id)
    
    if is_read is not None:
        query = query.where(Email.is_read == is_read)
        
    if priority:
        query = query.where(Email.priority_label == priority)

    query = query.order_by(Email.created_at.desc()).limit(limit)
    res = await db.execute(query)
    return res.scalars().all()

@router.post("/sync")
async def sync_emails(current_user: CurrentUser, db: DbSession):
    try:
        sync_service = GmailSyncService(db, current_user.id)
        sync_count = await sync_service.sync_recent_emails(limit=10)
        
        analyzed_count = 0
        try:
            ai_service = AIService(db)
            analyzed_count = await ai_service.analyze_unanalyzed_emails(current_user.id)
        except Exception as ai_error:
            print(f"AI Analysis failed: {ai_error}")
        
        return {"status": "success", "synced": sync_count, "analyzed": analyzed_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))