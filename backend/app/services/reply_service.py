from app.integrations.llm.provider import get_fast_llm
from app.models.email import Email
from langchain_core.messages import SystemMessage, HumanMessage

class ReplyService:
    def __init__(self):
        self.llm = get_fast_llm()

    async def generate_draft(self, email: Email, tone: str = "professional") -> str:
        prompt = [
            SystemMessage(content=f"You are an AI email assistant. Draft a {tone} reply to the following email. "
                                  "Do not include the subject line, just the body of the email. "
                                  "Keep it concise and helpful."),
            HumanMessage(content=f"From: {email.sender_name}\nSubject: {email.subject}\nSnippet: {email.snippet}")
        ]
        
        response = await self.llm.ainvoke(prompt)
        return response.content