from fastapi import APIRouter, Depends

from app.schemas.chat import ChatEntrada, ChatSalida
from app.services.llm import get_llm
from app.services.orquestador import responder

router = APIRouter()


# TODO: POST /chat (entrada ChatEntrada, salida ChatSalida). Recibe el LLM con Depends(get_llm)

@router.post("/chat")
def chat(chat: ChatEntrada, llm=Depends(get_llm)) -> ChatSalida:
    return responder(chat.mensajes, llm)