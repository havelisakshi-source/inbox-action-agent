import asyncio
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from app.api.deps import CurrentUser, DbSession
from app.models.email import Email
from app.models.action import Action, ActionHistory
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
        res = await db.execute(select(Email).where(Email.id == payload.email_id, Email.user_id == current_user.id))
        email = res.scalar_one_or_none()
        if not email:
            raise ValueError("Email not found")

        reply_service = ReplyService()
        draft_text = await reply_service.generate_draft(email, payload.tone)

        action = Action(
            user_id=current_user.id,
            email_id=email.id,
            action_type="draft_reply",
            payload={"draft_text": draft_text},
            reason=f"AI generated reply to {email.sender_name or 'sender'}",
            expected_outcome="Draft saved to Gmail",
            risk_level="moderate",
            status="executing",
            idempotency_key=str(uuid.uuid4())
        )
        db.add(action)
        await db.flush()

        sync_service = GmailSyncService(db, current_user.id)
        creds = await sync_service.get_credentials()
        service = await asyncio.to_thread(get_gmail_service, creds)
        
        draft_id = await asyncio.to_thread(
            create_gmail_draft,
            service=service,
            to_email=email.sender_email or "",
            subject=email.subject or "No Subject",
            body_text=draft_text,
            thread_id=email.thread_id
        )

        action.status = "executed"
        action.execution_result = {"gmail_draft_id": draft_id}
        
        history = ActionHistory(
            action_id=action.id,
            user_id=current_user.id,
            event="Draft created in Gmail",
            details={"draft_id": draft_id}
        )
        db.add(history)
        await db.commit()

        return DraftResponse(status="success", draft_text=draft_text)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_actions(current_user: CurrentUser, db: DbSession):
    res = await db.execute(
        select(Action)
        .where(Action.user_id == current_user.id)
        .order_by(Action.created_at.desc())
    )
    return res.scalars().all()