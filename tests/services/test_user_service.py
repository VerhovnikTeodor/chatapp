from unittest.mock import MagicMock
import bcrypt
from sqlalchemy.exc import IntegrityError

from app.schemas.user import UserCreate
from app.services.user_service import register_user, login_user, get_all_users


def _mock_db(first_return=None):
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = first_return
    return db


def test_register_user_success():
    db = _mock_db(first_return=None)
    payload = UserCreate(email="test@example.com", username="teodor", password="secret123")

    user = register_user(db, payload)

    assert user is not None
    assert user.email == payload.email
    assert user.username == payload.username
    assert isinstance(user.password, str)
    assert bcrypt.checkpw(payload.password.encode("utf-8"), user.password.encode("utf-8"))

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_register_user_duplicate_email_raises_value_error():
    db = _mock_db(first_return=MagicMock())
    payload = UserCreate(email="test@example.com", username="teodor", password="secret123")

    try:
        register_user(db, payload)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Email already registered"


def test_register_user_integrity_error():
    db = _mock_db(first_return=None)
    db.commit.side_effect = IntegrityError("stmt", "params", Exception("dup"))
    payload = UserCreate(email="test@example.com", username="teodor", password="secret123")

    result = register_user(db, payload)

    assert result is None
    db.rollback.assert_called_once()


def test_login_user_success():
    hashed = bcrypt.hashpw(b"secret123", bcrypt.gensalt()).decode("utf-8")
    fake_user = MagicMock()
    fake_user.email = "test@example.com"
    fake_user.password = hashed

    db = _mock_db(first_return=fake_user)

    result = login_user(db, "test@example.com", "secret123")
    assert result is fake_user


def test_login_user_wrong_password():
    hashed = bcrypt.hashpw(b"secret123", bcrypt.gensalt()).decode("utf-8")
    fake_user = MagicMock()
    fake_user.email = "test@example.com"
    fake_user.password = hashed

    db = _mock_db(first_return=fake_user)

    result = login_user(db, "test@example.com", "wrong-password")
    assert result is None


def test_login_user_missing_user_returns_none():
    db = _mock_db(first_return=None)

    result = login_user(db, "missing@example.com", "secret123")
    assert result is None


def test_get_all_users():
    db = MagicMock()
    expected = [MagicMock(), MagicMock()]
    db.query.return_value.all.return_value = expected

    result = get_all_users(db)

    assert result == expected