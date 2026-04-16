import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.db.session import Base, engine
from app.models.user import User
from app.models.chat import Chat, chat_members
from app.models.message import Message, MessageAttachment
from app.models.friends import Friend

from app.routers.auth import router as auth_router, require_auth
from app.routers import chat, friends, message, message_attachment
from .socketio import sio

Base.metadata.create_all(bind=engine)

fastapi_app = FastAPI()

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# public
fastapi_app.include_router(auth_router, prefix="/auth", tags=["auth"])

# protected
fastapi_app.include_router(chat.router, prefix="/chat", tags=["chat"], dependencies=[Depends(require_auth)])
fastapi_app.include_router(friends.router, prefix="/friends", tags=["friends"], dependencies=[Depends(require_auth)])
fastapi_app.include_router(message.router, prefix="/messages", tags=["messages"], dependencies=[Depends(require_auth)])
fastapi_app.include_router(message_attachment.router, prefix="/attachments", tags=["attachments"], dependencies=[Depends(require_auth)])

@fastapi_app.get("/")
def read_root():
    return {"Hello": "World"}

sio_app = socketio.ASGIApp(sio, fastapi_app)
app = sio_app