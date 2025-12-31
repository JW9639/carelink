"""Authentication service helpers."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    update_last_login,
)
from app.security.audit import AuditAction, log_action
from app.security.auth import hash_password, verify_password
from app.schemas.user import UserCreate
from app.models.user import User


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Authenticate a user and update last login."""
    user = get_user_by_email(db, email)
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    update_last_login(db, user.id)
    log_action(
        db=db,
        user_id=user.id,
        action=AuditAction.LOGIN,
        resource_type="user",
        resource_id=user.id,
        details={"email": user.email},
    )
    return user


def register_user(db: Session, user_create: UserCreate) -> User:
    """Register a new user."""
    user = create_user(db, user_create)
    log_action(
        db=db,
        user_id=user.id,
        action=AuditAction.CREATE_RECORD,
        resource_type="user",
        resource_id=user.id,
        details={"email": user.email},
    )
    return user


def change_password(
    db: Session, user_id: int, current_password: str, new_password: str
) -> bool:
    """Change a user's password if current password is valid."""
    user = get_user_by_id(db, user_id)
    if user is None:
        return False
    if not verify_password(current_password, user.hashed_password):
        return False
    user.hashed_password = hash_password(new_password)
    db.commit()
    log_action(
        db=db,
        user_id=user.id,
        action=AuditAction.UPDATE_RECORD,
        resource_type="user",
        resource_id=user.id,
        details={"field": "password"},
    )
    return True


def get_user_profile(db: Session, user_id: int) -> User | None:
    """Return a user profile."""
    return get_user_by_id(db, user_id)
