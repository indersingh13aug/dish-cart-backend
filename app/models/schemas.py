from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    user_message: str

class ChatResponse(BaseModel):
    assistant_message: str
    intent: str
