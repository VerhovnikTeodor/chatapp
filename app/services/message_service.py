from sqlalchemy.orm import Session
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate
import uuid


def get_messages(db: Session):
	return db.query(Message).all()


def get_message_by_id(db: Session, message_id: str):
	return db.query(Message).filter(Message.id == message_id).first()


def get_messages_by_chat_id(db: Session, chat_id: str):
	return db.query(Message).filter(Message.chatId == chat_id).all()


def create_message(db: Session, payload: MessageCreate):
	new_message = Message(
		id=str(uuid.uuid4()),
		content=payload.content,
		userId=payload.userId,
		chatId=payload.chatId,
	)
	db.add(new_message)
	db.commit()
	db.refresh(new_message)
	return new_message


def update_message(db: Session, message_id: str, payload: MessageUpdate):
	db_message = get_message_by_id(db, message_id)
	if not db_message:
		return None

	update_data = payload.model_dump(exclude_unset=True)
	for key, value in update_data.items():
		setattr(db_message, key, value)

	db.commit()
	db.refresh(db_message)
	return db_message


def delete_message(db: Session, message_id: str):
	db_message = get_message_by_id(db, message_id)
	if not db_message:
		return None

	db.delete(db_message)
	db.commit()
	return db_message

