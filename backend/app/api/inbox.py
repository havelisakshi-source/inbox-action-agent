from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.api.deps import CurrentUser, DbSession
from app.models.email import Email
from app.services.gmail_sync_service import GmailSyncService
from app.services.ai_service import AIService
from app.schemas.email import EmailResponse

router = APIRouter()

@router.get("", response_model=list[EmailResponse])
async def list_emails(current_user: CurrentUser, db: DbSession, limit: int = 20):
    res = await db.execute(
        select(Email)
        .where(Email.user_id == current_user.id)
        .order_by(Email.created_at.desc()) # Changed from received_at
        .limit(limit)
    )
    return res.scalars().all()

@router.post("/sync")
async def sync_emails(current_user: CurrentUser, db: DbSession):
    try:
        sync_service = GmailSyncService(db, current_user.id)
        sync_count = await sync_service.sync_recent_emails(limit=10)
        
        # Try analyzing, but don't crash if it fails
        analyzed_count = 0
        try:
            ai_service = AIService(db)
            analyzed_count = await ai_service.analyze_unanalyzed_emails(current_user.id)
        except Exception as ai_error:
            print(f"AI Analysis failed: {ai_error}")
        
        return {"status": "success", "synced": sync_count, "analyzed": analyzed_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))