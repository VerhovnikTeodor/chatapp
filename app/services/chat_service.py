from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatUpdate
import uuid


def get_chats(db: Session):
    return db.query(Chat).all()


def get_chat_by_id(db: Session, chat_id: str):
    return db.query(Chat).filter(Chat.id == chat_id).first()


def create_chat(db: Session, payload: ChatCreate):
    new_chat = Chat(
        id=str(uuid.uuid4()),
        name=payload.name,
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


def update_chat(db: Session, chat_id: str, payload: ChatUpdate):
    db_chat = get_chat_by_id(db, chat_id)
    if not db_chat:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_chat, key, value)

    db.commit()
    db.refresh(db_chat)
    return db_chat


def delete_chat(db: Session, chat_id: str):
    db_chat = get_chat_by_id(db, chat_id)
    if not db_chat:
        return None

    db.delete(db_chat)
    db.commit()
    return db_chat
