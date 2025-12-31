"""Tests for authentication utilities."""

from app.security.auth import generate_session_token, hash_password, verify_password
from app.services.auth_service import authenticate_user, change_password


def test_hash_password_salts():
    pw = "MySecurePass1!"
    hash1 = hash_password(pw)
    hash2 = hash_password(pw)
    assert hash1 != hash2


def test_verify_password_success():
    pw = "AnotherPass1!"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed)


def test_verify_password_failure():
    pw = "Pass123!"
    hashed = hash_password(pw)
    assert not verify_password("wrong", hashed)


def test_generate_session_token_uniqueness():
    token1 = generate_session_token()
    token2 = generate_session_token()
    assert token1 != token2


def test_authenticate_user_success(test_db, test_user):
    user = authenticate_user(test_db, test_user.email, "Patient123!")
    assert user is not None
    assert user.id == test_user.id


def test_authenticate_user_wrong_password(test_db, test_user):
    user = authenticate_user(test_db, test_user.email, "WrongPass123!")
    assert user is None


def test_authenticate_user_inactive(test_db, test_user):
    test_user.is_active = False
    test_db.commit()
    user = authenticate_user(test_db, test_user.email, "Patient123!")
    assert user is None


def test_authenticate_user_not_found(test_db):
    user = authenticate_user(test_db, "missing@example.com", "TestPass123!")
    assert user is None


def test_change_password_success(test_db, test_user):
    assert change_password(test_db, test_user.id, "Patient123!", "NewPass123!")
    test_db.refresh(test_user)
    assert verify_password("NewPass123!", test_user.hashed_password)


def test_change_password_wrong_current(test_db, test_user):
    assert not change_password(test_db, test_user.id, "WrongPass", "NewPass123!")
