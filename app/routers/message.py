import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.message import MessageCreate, MessageUpdate, Message as MessageSchema
from app.services.message_service import (
	get_messages,
	get_message_by_id,
	get_messages_by_chat_id,
	create_message,
	update_message,
	delete_message,
)


router = APIRouter()
logger = logging.getLogger(__name__)


def _error(status_code: int, code: str, message: str) -> HTTPException:
	return HTTPException(status_code=status_code, detail={"code": code, "message": message})


@router.get("/", response_model=list[MessageSchema])
def list_messages(db: Session = Depends(get_db)):
	try:
		return get_messages(db)
	except Exception:
		logger.exception("List messages failed")
		raise _error(500, "MESSAGES_FETCH_FAILED", "Napaka pri pridobivanju sporočil")


@router.get("/{message_id}", response_model=MessageSchema)
def get_message(message_id: str, db: Session = Depends(get_db)):
	try:
		message = get_message_by_id(db, message_id)
	except Exception:
		logger.exception("Get message failed")
		raise _error(500, "MESSAGE_FETCH_FAILED", "Napaka pri pridobivanju sporočila")

	if not message:
		raise _error(404, "MESSAGE_NOT_FOUND", "Message not found")
	return message


@router.get("/chat/{chat_id}", response_model=list[MessageSchema])
def list_chat_messages(chat_id: str, db: Session = Depends(get_db)):
	try:
		return get_messages_by_chat_id(db, chat_id)
	except Exception:
		logger.exception("List chat messages failed")
		raise _error(500, "CHAT_MESSAGES_FETCH_FAILED", "Napaka pri pridobivanju sporočil chata")


@router.post("/", response_model=MessageSchema)
def post_message(payload: MessageCreate, db: Session = Depends(get_db)):
	try:
		return create_message(db, payload)
	except Exception:
		logger.exception("Create message failed")
		raise _error(500, "MESSAGE_CREATE_FAILED", "Napaka pri ustvarjanju sporočila")


@router.put("/{message_id}", response_model=MessageSchema)
def put_message(message_id: str, payload: MessageUpdate, db: Session = Depends(get_db)):
	try:
		message = update_message(db, message_id, payload)
	except Exception:
		logger.exception("Update message failed")
		raise _error(500, "MESSAGE_UPDATE_FAILED", "Napaka pri posodobitvi sporočila")

	if not message:
		raise _error(404, "MESSAGE_NOT_FOUND", "Message not found")
	return message


@router.delete("/{message_id}", response_model=MessageSchema)
def remove_message(message_id: str, db: Session = Depends(get_db)):
	try:
		message = delete_message(db, message_id)
	except Exception:
		logger.exception("Delete message failed")
		raise _error(500, "MESSAGE_DELETE_FAILED", "Napaka pri brisanju sporočila")

	if not message:
		raise _error(404, "MESSAGE_NOT_FOUND", "Message not found")
	return message

