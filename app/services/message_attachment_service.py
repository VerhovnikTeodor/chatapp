from sqlalchemy.orm import Session
from app.models.message import MessageAttachment
from app.schemas.message import MessageAttachmentCreate, MessageAttachmentUpdate
import uuid


def get_message_attachments(db: Session):
    return db.query(MessageAttachment).all()


def get_message_attachment_by_id(db: Session, attachment_id: str):
    return db.query(MessageAttachment).filter(MessageAttachment.id == attachment_id).first()


def get_message_attachments_by_message_id(db: Session, message_id: str):
    return (
        db.query(MessageAttachment)
        .filter(MessageAttachment.messageId == message_id)
        .all()
    )


def create_message_attachment(db: Session, payload: MessageAttachmentCreate, message_id: str):
    new_attachment = MessageAttachment(
        id=str(uuid.uuid4()),
        messageId=message_id,
        url=payload.url,
        mediaType=payload.mediaType,
    )
    db.add(new_attachment)
    db.commit()
    db.refresh(new_attachment)
    return new_attachment


def update_message_attachment(db: Session, attachment_id: str, payload: MessageAttachmentUpdate):
    db_attachment = get_message_attachment_by_id(db, attachment_id)
    if not db_attachment:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_attachment, key, value)

    db.commit()
    db.refresh(db_attachment)
    return db_attachment


def delete_message_attachment(db: Session, attachment_id: str):
    db_attachment = get_message_attachment_by_id(db, attachment_id)
    if not db_attachment:
        return None

    db.delete(db_attachment)
    db.commit()
    return db_attachment
