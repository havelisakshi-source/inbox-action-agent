import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from app.api.deps import CurrentUser, DbSession
from app.models.email import Email
from app.services.reply_service import ReplyService
from app.services.gmail_sync_service import GmailSyncService
from app.integrations.gmail.client import get_gmail_service, create_gmail_draft

router = APIRouter()

class DraftRequest(BaseModel):
    email_id: str
    tone: str = "professional"

class DraftResponse(BaseModel):
    status: str
    draft_text: str

@router.post("/draft", response_model=DraftResponse)
async def create_draft(payload: DraftRequest, current_user: CurrentUser, db: DbSession):
    try:
        # 1. Get the email
        res = await db.execute(select(Email).where(Email.id == payload.email_id, Email.user_id == current_user.id))
        email = res.scalar_one_or_none()
        if not email:
            raise ValueError("Email not found")

        # 2. Generate the text with AI
        reply_service = ReplyService()
        draft_text = await reply_service.generate_draft(email, payload.tone)

        # 3. Save to Gmail
        sync_service = GmailSyncService(db, current_user.id)
        creds = await sync_service.get_credentials()
        service = await asyncio.to_thread(get_gmail_service, creds)
        
        # Run the blocking Gmail API call in a separate thread
        await asyncio.to_thread(
            create_gmail_draft,
            service=service,
            to_email=email.sender_email or "",
            subject=email.subject or "No Subject",
            body_text=draft_text,
            thread_id=email.thread_id
        )

        return DraftResponse(status="success", draft_text=draft_text)
    except Exception as e:
        # Return a clean JSON error to the frontend
        raise HTTPException(status_code=500, detail=str(e))