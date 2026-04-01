import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

@sio.event
async def connect(sid, environ):
    print(f"Povezan: {sid}")
    await sio.emit('pozdrav', {'sporocilo': 'Pozdravljen s strežnika!'}, to=sid)


@sio.event
async def disconnect(sid):
    print(f"Povezava prekinjena: {sid}")

@sio.on('chat_message')
async def handle_chat_message(sid, data):
    print(f"Prejeto sporočilo od {sid}: {data}")
