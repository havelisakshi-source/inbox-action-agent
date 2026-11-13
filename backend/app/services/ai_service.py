import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.email import Email
from app.integrations.llm.provider import get_fast_llm
from app.core.logging import get_logger

log = get_logger(__name__)

PROMPT_TEMPLATE = """
You are an AI email assistant. Analyze the following email and return a JSON object.
DO NOT wrap the JSON in markdown formatting. Just return the raw JSON.

Email Subject: {subject}
Email Snippet: {snippet}

Return a JSON with exactly these keys:
- "category": One of ["Work", "Education", "Personal", "Finance", "Promotions", "Newsletters", "Spam", "Other"]
- "priority_score": An integer from 1 to 100 (100 is extremely urgent, 1 is spam).
- "summary_short": A 1-sentence summary of what the email is about.
- "needs_reply": Boolean (true if the email contains a direct question or requires the user to respond, false otherwise).
"""

class AIService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.llm = get_fast_llm()

    async def analyze_email(self, email: Email) -> None:
        prompt = PROMPT_TEMPLATE.format(
            subject=email.subject or "(No Subject)",
            snippet=email.snippet or ""
        )
        
        try:
            response = await self.llm.ainvoke(prompt)
            content = response.content.strip()
            
            # Clean up markdown formatting
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            
            data = json.loads(content)
            
            email.category = data.get("category", "Other")
            email.priority_score = data.get("priority_score", 50)
            email.summary_short = data.get("summary_short", "")
            email.needs_reply = data.get("needs_reply", False)
            
            if email.priority_score >= 80:
                email.priority_label = "high"
            elif email.priority_score >= 40:
                email.priority_label = "normal"
            else:
                email.priority_label = "low"
                
        except Exception as e:
            print(f"\n--- AI ERROR ---\n{str(e)}\n----------------\n")
            log.error("ai_analysis_failed", email_id=email.id, error=str(e))
            email.category = "Other"
            email.priority_score = 50
            email.priority_label = "normal"
            email.summary_short = email.snippet
            email.needs_reply = False

    async def analyze_unanalyzed_emails(self, user_id: str) -> int:
        res = await self.db.execute(
            select(Email).where(
                Email.user_id == user_id, 
                or_(Email.category == None, Email.needs_reply == None)
            ).limit(15)
        )
        emails = res.scalars().all()
        
        for email in emails:
            await self.analyze_email(email)
            
        await self.db.commit()
        return len(emails)