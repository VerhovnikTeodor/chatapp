from fastapi import FastAPI
from app.db.session import engine
from app.models import user
from app.routers import auth
from .socketio import sio
import socketio

user.Base.metadata.create_all(bind=engine)

app = FastAPI()

sio_app = socketio.ASGIApp(sio, app)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
