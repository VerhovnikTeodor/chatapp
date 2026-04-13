import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.chat import ChatCreate, ChatUpdate, Chat as ChatSchema
from app.services.chat_service import (
    get_chats,
    get_chat_by_id,
    create_chat,
    update_chat,
    delete_chat,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


@router.get("/", response_model=list[ChatSchema])
def list_chats(db: Session = Depends(get_db)):
    try:
        return get_chats(db)
    except Exception:
        logger.exception("List chats failed")
        raise _error(500, "CHATS_FETCH_FAILED", "Napaka pri pridobivanju chatov")


@router.get("/{chat_id}", response_model=ChatSchema)
def get_chat(chat_id: str, db: Session = Depends(get_db)):
    try:
        chat = get_chat_by_id(db, chat_id)
    except Exception:
        logger.exception("Get chat failed")
        raise _error(500, "CHAT_FETCH_FAILED", "Napaka pri pridobivanju chata")

    if not chat:
        raise _error(404, "CHAT_NOT_FOUND", "Chat not found")
    return chat


@router.post("/", response_model=ChatSchema)
def post_chat(payload: ChatCreate, db: Session = Depends(get_db)):
    try:
        return create_chat(db, payload)
    except Exception:
        logger.exception("Create chat failed")
        raise _error(500, "CHAT_CREATE_FAILED", "Napaka pri ustvarjanju chata")


@router.put("/{chat_id}", response_model=ChatSchema)
def put_chat(chat_id: str, payload: ChatUpdate, db: Session = Depends(get_db)):
    try:
        chat = update_chat(db, chat_id, payload)
    except Exception:
        logger.exception("Update chat failed")
        raise _error(500, "CHAT_UPDATE_FAILED", "Napaka pri posodobitvi chata")

    if not chat:
        raise _error(404, "CHAT_NOT_FOUND", "Chat not found")
    return chat


@router.delete("/{chat_id}", response_model=ChatSchema)
def remove_chat(chat_id: str, db: Session = Depends(get_db)):
    try:
        chat = delete_chat(db, chat_id)
    except Exception:
        logger.exception("Delete chat failed")
        raise _error(500, "CHAT_DELETE_FAILED", "Napaka pri brisanju chata")

    if not chat:
        raise _error(404, "CHAT_NOT_FOUND", "Chat not found")
    return chat
