from fastapi import APIRouter
from pydantic import BaseModel
from app.api.deps import CurrentUser, DbSession
from app.agents.assistant_graph import create_agent_executor
from langchain_core.messages import HumanMessage

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(payload: ChatRequest, current_user: CurrentUser, db: DbSession):
    agent = await create_agent_executor(db, current_user.id)
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=payload.message)]}
    )
    final_message = result["messages"][-1].content
    return ChatResponse(response=final_message)