from fastapi import APIRouter,status
from src.Chatbot import controller
from src.Chatbot.dtos import ChatResponse

chat_router = APIRouter(prefix="/chat")

@chat_router.get("/ask",response_model=ChatResponse,status_code=status.HTTP_200_OK)
def chat(user_input: str):
    response = controller.chatbot(user_input)

    return  response
