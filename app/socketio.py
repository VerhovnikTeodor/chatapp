import socketio
import logging
from app.db.session import SessionLocal
from app.schemas.message import MessageCreate
from app.services.message_service import create_message



logging.basicConfig(level=logging.INFO)
log = logging.getLogger("chatapp.socketio")

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
)


@sio.event
async def connect(sid, environ):
    log.info(f"Povezan: {sid}")
    await sio.emit('pozdrav', {'sporocilo': 'Pozdravljen s strežnika!'}, to=sid)


@sio.event
async def disconnect(sid):
    log.info(f"Povezava prekinjena: {sid}")

@sio.on("chat_message")
async def receive_chat_message(sid, data):
    db = SessionLocal()
    try:
        payload = MessageCreate(
            chatId=data["chatId"],
            userId=data["userId"],
            content=data.get("content"),
        )
        message = create_message(db, payload)

        event_payload = {
            "id": message.id,
            "chatId": message.chatId,
            "userId": message.userId,
            "content": message.content,
            "createdAt": str(message.createdAt),
        }

        await sio.emit("chat_message", event_payload, room=message.chatId)
        return {"ok": True, "messageId": message.id}
    except Exception:
        log.exception("chat_message handler failed")
        return {"ok": False}
    finally:
        db.close()