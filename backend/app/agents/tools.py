from typing import Optional
from langchain_core.tools import tool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.email import Email

def create_email_tools(db: AsyncSession, user_id: str):
    """Factory function to create tools bound to a specific user and DB session."""
    
    @tool
    async def get_recent_emails(category: Optional[str] = None, limit: int = 5) -> str:
        """Fetch the most recent emails from the user's inbox. You can optionally filter by category (e.g., 'Work', 'Promotions', 'Education')."""
        query = select(Email).where(Email.user_id == user_id)
        
        if category:
            query = query.where(Email.category.ilike(f"%{category}%"))
            
        query = query.order_by(Email.received_at.desc().nulls_last()).limit(limit)
        
        result = await db.execute(query)
        emails = result.scalars().all()
        
        if not emails:
            return "No emails found."
            
        output = []
        for e in emails:
            output.append(
                f"From: {e.sender_name} <{e.sender_email}>\n"
                f"Subject: {e.subject}\n"
                f"Category: {e.category}\n"
                f"Summary: {e.summary_short}\n"
                f"Snippet: {e.snippet}\n"
                f"---"
            )
        return "\n".join(output)

    return [get_recent_emails]