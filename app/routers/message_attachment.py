import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.message import (
    MessageAttachmentCreate,
    MessageAttachmentUpdate,
    MessageAttachment as MessageAttachmentSchema,
)
from app.services.message_attachment_service import (
    get_message_attachments,
    get_message_attachment_by_id,
    get_message_attachments_by_message_id,
    create_message_attachment,
    update_message_attachment,
    delete_message_attachment,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


@router.get("/", response_model=list[MessageAttachmentSchema])
def list_attachments(db: Session = Depends(get_db)):
    try:
        return get_message_attachments(db)
    except Exception:
        logger.exception("List attachments failed")
        raise _error(500, "ATTACHMENTS_FETCH_FAILED", "Napaka pri pridobivanju attachmentov")


@router.get("/{attachment_id}", response_model=MessageAttachmentSchema)
def get_attachment(attachment_id: str, db: Session = Depends(get_db)):
    try:
        attachment = get_message_attachment_by_id(db, attachment_id)
    except Exception:
        logger.exception("Get attachment failed")
        raise _error(500, "ATTACHMENT_FETCH_FAILED", "Napaka pri pridobivanju attachmenta")

    if not attachment:
        raise _error(404, "ATTACHMENT_NOT_FOUND", "Attachment not found")
    return attachment


@router.get("/message/{message_id}", response_model=list[MessageAttachmentSchema])
def list_message_attachments(message_id: str, db: Session = Depends(get_db)):
    try:
        return get_message_attachments_by_message_id(db, message_id)
    except Exception:
        logger.exception("List message attachments failed")
        raise _error(500, "MESSAGE_ATTACHMENTS_FETCH_FAILED", "Napaka pri pridobivanju attachmentov sporočila")


@router.post("/message/{message_id}", response_model=MessageAttachmentSchema)
def post_attachment(message_id: str, payload: MessageAttachmentCreate, db: Session = Depends(get_db)):
    try:
        return create_message_attachment(db, payload, message_id)
    except Exception:
        logger.exception("Create attachment failed")
        raise _error(500, "ATTACHMENT_CREATE_FAILED", "Napaka pri ustvarjanju attachmenta")


@router.put("/{attachment_id}", response_model=MessageAttachmentSchema)
def put_attachment(attachment_id: str, payload: MessageAttachmentUpdate, db: Session = Depends(get_db)):
    try:
        attachment = update_message_attachment(db, attachment_id, payload)
    except Exception:
        logger.exception("Update attachment failed")
        raise _error(500, "ATTACHMENT_UPDATE_FAILED", "Napaka pri posodobitvi attachmenta")

    if not attachment:
        raise _error(404, "ATTACHMENT_NOT_FOUND", "Attachment not found")
    return attachment


@router.delete("/{attachment_id}", response_model=MessageAttachmentSchema)
def remove_attachment(attachment_id: str, db: Session = Depends(get_db)):
    try:
        attachment = delete_message_attachment(db, attachment_id)
    except Exception:
        logger.exception("Delete attachment failed")
        raise _error(500, "ATTACHMENT_DELETE_FAILED", "Napaka pri brisanju attachmenta")

    if not attachment:
        raise _error(404, "ATTACHMENT_NOT_FOUND", "Attachment not found")
    return attachment
