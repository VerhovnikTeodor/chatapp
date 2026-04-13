from fastapi import FastAPI
from app.db.session import Base, engine
from app.models.user import User
from app.models.chat import Chat, chat_members
from app.models.message import Message, MessageAttachment
from app.models.friends import Friend
from app.routers import auth
from app.routers import chat
from app.routers import friends
from app.routers import message
from app.routers import message_attachment
from .socketio import sio
import socketio

Base.metadata.create_all(bind=engine)

app = FastAPI()

sio_app = socketio.ASGIApp(sio, app)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(friends.router, prefix="/friends", tags=["friends"])
app.include_router(message.router, prefix="/messages", tags=["messages"])
app.include_router(message_attachment.router, prefix="/attachments", tags=["attachments"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
