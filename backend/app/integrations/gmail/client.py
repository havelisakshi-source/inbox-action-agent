from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from email.message import EmailMessage

def get_gmail_service(creds: Credentials):
    return build("gmail", "v1", credentials=creds, cache_discovery=False)

def fetch_messages_list(service, max_results: int = 20):
    """Fetches a list of message IDs from the user's entire mailbox."""
    results = service.users().messages().list(
        userId="me", 
        maxResults=max_results
    ).execute()
    return results.get("messages", [])

def fetch_message_detail(service, message_id: str):
    """Fetches full details of a single message."""
    return service.users().messages().get(
        userId="me", 
        id=message_id, 
        format="metadata",
        metadataHeaders=["From", "Subject", "Date"]
    ).execute()

def create_gmail_draft(service, to_email: str, subject: str, body_text: str, thread_id: str | None = None):
    """Creates a draft in the user's Gmail account."""
    message = EmailMessage()
    message.set_content(body_text)
    message["To"] = to_email
    
    safe_subject = subject if subject.lower().startswith("re:") else f"Re: {subject}"
    message["Subject"] = safe_subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    create_message = {
        "message": {
            "raw": encoded_message,
        }
    }
    
    if thread_id:
        create_message["message"]["threadId"] = thread_id

    draft = service.users().drafts().create(userId="me", body=create_message).execute()
    return draft["id"]