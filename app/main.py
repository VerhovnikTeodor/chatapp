from fastapi import FastAPI
from app.db.session import engine
from app.models import user
from app.routers import auth

user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
