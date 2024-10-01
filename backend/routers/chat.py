from fastapi import APIRouter
from .. import schemas
from ..services.agent import chat as agent_chat
from llama_index.core.base.llms.types import ChatMessage, MessageRole

router = APIRouter()

@router.post("/chat/", response_model=schemas.ChatResponse)
async def chat(request: schemas.ChatRequest):
    chat_history = [ChatMessage(role=MessageRole(msg.role), content=msg.content) for msg in request.history_messages[:-1]]
    latest_message = request.history_messages[-1].content if request.history_messages else ""
    response = await agent_chat(latest_message, chat_history)
    return schemas.ChatResponse(
        message=schemas.Message(role=schemas.MessageRole.ASSISTANT, content=response)
    )