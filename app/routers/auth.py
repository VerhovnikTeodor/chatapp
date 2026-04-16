# ...existing code...
import logging
import os

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.config import settings

from app.db.session import get_db
from app.schemas.user import UserCreate, User, UserLogin, LoginResponse
from app.services.jwt_service import create_access_token, verify_access_token
from app.services.user_service import get_all_users, login_user, register_user

router = APIRouter()
logger = logging.getLogger(__name__)
bearer_scheme = HTTPBearer(auto_error=False)

COOKIE_NAME = "access_token"
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"  # local dev: false
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "lax")  # lax/strict/none


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


def _extract_token(request: Request, creds: HTTPAuthorizationCredentials | None) -> str | None:
    if creds and creds.scheme.lower() == "bearer":
        return creds.credentials

    cookie_token = request.cookies.get(COOKIE_NAME)
    if cookie_token:
        if cookie_token.lower().startswith("bearer "):
            return cookie_token.split(" ", 1)[1]
        return cookie_token

    return None


def require_auth(
    request: Request,
    creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    token = _extract_token(request, creds)
    if not token:
        raise _error(status.HTTP_401_UNAUTHORIZED, "AUTH_MISSING", "Manjka prijava")

    payload = verify_access_token(token)
    if not payload or not payload.get("sub"):
        raise _error(status.HTTP_401_UNAUTHORIZED, "AUTH_INVALID", "Neveljaven ali potekel token")

    return payload["sub"]  # user_id iz "sub"


@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = register_user(db=db, user=user)
    except ValueError as e:
        raise _error(400, "REGISTER_INVALID", str(e))
    except Exception:
        logger.exception("Register failed")
        raise _error(500, "REGISTER_FAILED", "Napaka pri registraciji uporabnika")

    if db_user is None:
        raise _error(400, "REGISTER_FAILED", "Registracija ni uspela")
    return db_user


@router.post("/login", response_model=LoginResponse)
def login(payload: UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        user = login_user(db=db, email=payload.email, entered_password=payload.password)
    except Exception:
        logger.exception("Login failed")
        raise _error(500, "LOGIN_FAILED", "Napaka pri prijavi")

    if user is None:
        raise _error(status.HTTP_401_UNAUTHORIZED, "LOGIN_INVALID", "Napačen email ali geslo")

    token = create_access_token(subject=user.id)

    cookie_max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    # HttpOnly cookie 
    response.set_cookie(
        key=COOKIE_NAME,
        value=f"Bearer {token}",
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=cookie_max_age,
        path="/",
    )
    
    return LoginResponse(success=True, access_token=token, token_type="bearer")


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME, path="/")
    return {"success": True}


@router.get("/me")
def me(current_user_id: str = Depends(require_auth)):
    return {"userId": current_user_id}


@router.get("/users", response_model=list[User])
def get_users(
    db: Session = Depends(get_db),
    _current_user_id: str = Depends(require_auth),  
):
    try:
        return get_all_users(db=db)
    except Exception:
        logger.exception("Get users failed")
        raise _error(500, "USERS_FETCH_FAILED", "Napaka pri pridobivanju uporabnikov")
