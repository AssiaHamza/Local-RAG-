from fastapi import APIRouter
from pydantic import BaseModel
from rag.pipeline import ask

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    question: str
    session_id: str

@router.post("/")
def chat(request: ChatRequest):
    answer = ask(question=request.question, session_id=request.session_id)
    return answer