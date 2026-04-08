import socketio
import logging


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


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

@sio.on('chat_message')
async def handle_chat_message(sid, data):
    log.info(f"Prejeto sporočilo od {sid}: {data}")
    await sio.emit('chat_message', data)
    return {"ok": True}