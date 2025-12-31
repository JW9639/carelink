"""Tests for authentication utilities."""

from app.security.auth import (
    generate_session_token,
    hash_password,
    verify_password,
)


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
