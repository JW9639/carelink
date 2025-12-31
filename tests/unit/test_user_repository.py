"""Tests for user repository functions."""

import pytest

from app.db.repositories.user_repository import (
    create_user,
    deactivate_user,
    get_user_by_email,
    get_users_by_role,
    update_last_login,
)
from app.schemas.user import UserCreate
from app.utils.constants import UserRole


def test_create_user(test_db):
    """Test creating a new user."""
    user_data = UserCreate(
        email="test@example.com",
        password="TestPass123!",
        role=UserRole.PATIENT,
    )
    user = create_user(test_db, user_data)
    assert user.email == "test@example.com"
    assert user.hashed_password != "TestPass123!"


def test_get_user_by_email(test_db, test_user):
    """Test retrieving user by email."""
    user = get_user_by_email(test_db, test_user.email)
    assert user is not None
    assert user.id == test_user.id


def test_get_user_by_email_not_found(test_db):
    """Test retrieving non-existent user."""
    user = get_user_by_email(test_db, "nonexistent@example.com")
    assert user is None


def test_duplicate_email_raises_error(test_db, test_user):
    """Test that duplicate email raises error."""
    user_data = UserCreate(
        email=test_user.email,
        password="AnotherPass123!",
        role=UserRole.PATIENT,
    )
    with pytest.raises(Exception):
        create_user(test_db, user_data)
    test_db.rollback()


def test_update_last_login(test_db, test_user):
    """Test updating last login timestamp."""
    update_last_login(test_db, test_user.id)
    test_db.refresh(test_user)
    assert test_user.last_login is not None


def test_deactivate_user(test_db, test_user):
    """Test deactivating a user."""
    deactivate_user(test_db, test_user.id)
    test_db.refresh(test_user)
    assert test_user.is_active is False


def test_get_users_by_role(test_db, test_user):
    """Test getting users by role."""
    users = get_users_by_role(test_db, UserRole.PATIENT)
    assert len(users) >= 1
    assert all(u.role == UserRole.PATIENT for u in users)
