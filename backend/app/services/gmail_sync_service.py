import asyncio
import email.utils
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from app.core.config import settings
from app.core.security import decrypt_token, encrypt_token
from app.models.user import OAuthCredential
from app.models.email import Email
from app.integrations.gmail.client import get_gmail_service, fetch_messages_list, fetch_message_detail
from app.core.logging import get_logger

log = get_logger(__name__)

class GmailSyncService:
    def __init__(self, db: AsyncSession, user_id: str):
        self.db = db
        self.user_id = user_id

    async def get_credentials(self) -> Credentials | None:
        res = await self.db.execute(select(OAuthCredential).where(OAuthCredential.user_id == self.user_id))
        cred = res.scalar_one_or_none()
        if not cred:
            return None
        
        access = decrypt_token(cred.encrypted_access_token)
        refresh = decrypt_token(cred.encrypted_refresh_token) if cred.encrypted_refresh_token else None
        
        creds = Credentials(
            token=access,
            refresh_token=refresh,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=settings.GMAIL_SCOPES,
        )

        if not creds.valid:
            if creds.expired and creds.refresh_token:
                await asyncio.to_thread(creds.refresh, Request())
                cred.encrypted_access_token = encrypt_token(creds.token)
                await self.db.commit()
            else:
                raise ValueError("Gmail credentials are invalid. Please reconnect in Settings.")

        return creds

    async def sync_recent_emails(self, limit: int = 10) -> int:
        creds = await self.get_credentials()
        if not creds:
            raise ValueError("No Gmail credentials found. Please reconnect Gmail in Settings.")

        service = await asyncio.to_thread(get_gmail_service, creds)
        messages = await asyncio.to_thread(fetch_messages_list, service, limit)
        
        print(f"\n--- SYNC DEBUG: Found {len(messages)} messages from Gmail for user {self.user_id} ---\n")
        
        synced_count = 0
        for msg in messages:
            res = await self.db.execute(select(Email).where(Email.gmail_message_id == msg["id"]))
            if res.scalar_one_or_none():
                print(f"DEBUG: Email {msg['id']} already exists in DB, skipping.")
                continue

            print(f"DEBUG: Processing new email {msg['id']}")
            detail = await asyncio.to_thread(fetch_message_detail, service, msg["id"])
            headers = {h["name"]: h["value"] for h in detail["payload"]["headers"]}
            
            sender_raw = headers.get("From", "")
            sender_name, sender_email = email.utils.parseaddr(sender_raw)
            
            internal_date = detail.get("internalDate")
            received_at = None
            if internal_date:
                received_at = datetime.fromtimestamp(int(internal_date) / 1000.0, tz=timezone.utc)

            new_email = Email(
                user_id=self.user_id,
                gmail_message_id=msg["id"],
                thread_id=msg["threadId"],
                sender_name=sender_name,
                sender_email=sender_email,
                subject=headers.get("Subject", "(No Subject)"),
                snippet=detail.get("snippet", ""),
                received_at=received_at, 
                is_read="UNREAD" not in detail.get("labelIds", []),
                is_starred="STARRED" in detail.get("labelIds", []),
                has_attachment="attachment" in str(detail["payload"].get("parts", [])).lower(),
                gmail_label_ids=detail.get("labelIds", []),
            )
            self.db.add(new_email)
            synced_count += 1

        await self.db.commit()
        print(f"--- SYNC DEBUG: Successfully saved {synced_count} new emails ---\n")
        return synced_count