from pydantic import BaseModel
from datetime import datetime

class EmailResponse(BaseModel):
    id: str
    gmail_message_id: str
    sender_name: str | None
    sender_email: str | None
    subject: str | None
    snippet: str | None
    received_at: datetime | None
    is_read: bool
    is_starred: bool
    has_attachment: bool

    # Add the AI fields here!
    category: str | None
    priority_score: int | None
    priority_label: str | None
    summary_short: str | None

    model_config = {"from_attributes": True}