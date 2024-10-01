from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel):
    role: MessageRole
    content: str

class ChatRequest(BaseModel):
    history_messages: List[Message]

class ChatResponse(BaseModel):
    message: Message
    
class ToolScore(BaseModel):
    tool_name: str
    description: str
    website: Optional[str] = None
    reasons: List[str]
    score: int

class ScoreboardResponse(BaseModel):
    top_tools: List[ToolScore]
