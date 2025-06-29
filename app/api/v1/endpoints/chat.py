from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.core.orchestrator import orchestrate

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    return orchestrate(payload.user_id, payload.user_message)
