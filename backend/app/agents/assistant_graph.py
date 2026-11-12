from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from app.core.config import settings
from app.agents.tools import create_email_tools
from sqlalchemy.ext.asyncio import AsyncSession

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

async def create_agent_executor(db: AsyncSession, user_id: str):
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL_REASONING,
        temperature=0.2,
    )
    
    tools = create_email_tools(db, user_id)
    llm_with_tools = llm.bind_tools(tools)

    async def agent_node(state: AgentState):
        system_prompt = SystemMessage(
            content="You are a helpful AI email assistant. Use the tools provided to answer the user's questions about their inbox. Keep answers concise and helpful."
        )
        messages = [system_prompt] + state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    def should_continue(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))

    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")

    return workflow.compile()