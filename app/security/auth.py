"""Authentication utilities."""

from __future__ import annotations

import secrets
from typing import Final

import bcrypt

from app.config import get_settings

settings = get_settings()


def get_password_hash_rounds() -> int:
    """Return configured bcrypt rounds."""
    return settings.BCRYPT_ROUNDS


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    rounds: Final[int] = get_password_hash_rounds()
    salt = bcrypt.gensalt(rounds)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a stored hash."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode())
    except ValueError:
        return False


def generate_session_token() -> str:
    """Generate a cryptographically secure session token."""
    return secrets.token_urlsafe(32)
