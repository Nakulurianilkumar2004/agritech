from fastapi import APIRouter, Depends, HTTPException
from app.modules.chatbot.schemas import ChatRequest, ChatResponse
from app.modules.chatbot.service import process_chat
from app.modules.chatbot.rag_retriever import load_rag_data
from app.core.dependencies import get_current_user

router = APIRouter()

# Load RAG data
load_rag_data()

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    user=Depends(get_current_user)  # any logged-in user allowed
):
    if not request.message:
        raise HTTPException(status_code=400, detail="No message provided")

    result = process_chat(request.message, request.mode)
    return result