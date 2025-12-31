"""User repository helpers."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.security.auth import hash_password
from app.utils.constants import UserRole


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Fetch a user by primary key."""
    return db.execute(select(User).where(User.id == user_id)).scalars().first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Fetch a user by email address."""
    return db.execute(select(User).where(User.email == email)).scalars().first()


def create_user(db: Session, user_create: UserCreate) -> User:
    """Create a user with hashed password."""
    user = User(
        email=user_create.email,
        hashed_password=hash_password(user_create.password),
        role=user_create.role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_last_login(db: Session, user_id: int) -> None:
    """Update the last login timestamp."""
    user = get_user_by_id(db, user_id)
    if user is None:
        return
    user.last_login = datetime.now(timezone.utc)
    db.commit()


def deactivate_user(db: Session, user_id: int) -> None:
    """Deactivate a user account."""
    user = get_user_by_id(db, user_id)
    if user is None:
        return
    user.is_active = False
    db.commit()


def get_users_by_role(
    db: Session, role: UserRole, skip: int = 0, limit: int = 7
) -> list[User]:
    """Return users filtered by role."""
    query = select(User).where(User.role == role).offset(skip).limit(limit)
    return list(db.execute(query).scalars().all())
