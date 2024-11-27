from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    user_id: int

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    # TODO: 接入Grok API
    reply = f"你说: {message.message}"
    return ChatResponse(reply=reply) 