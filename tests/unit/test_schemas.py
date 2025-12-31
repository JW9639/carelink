"""Tests for Pydantic schemas."""

import pytest

from app.schemas.profile import PasswordChange
from app.schemas.user import UserCreate
from app.utils.constants import UserRole


def test_user_create_password_validator():
    with pytest.raises(ValueError):
        UserCreate(email="user@example.com", role=UserRole.PATIENT, password="short")


def test_password_change_validation():
    payload = PasswordChange(
        current_password="OldPass1!",
        new_password="NewPass123!",
        confirm_password="NewPass123!",
    )
    assert payload.new_password == "NewPass123!"

    with pytest.raises(ValueError):
        PasswordChange(
            current_password="OldPass1!",
            new_password="weak",
            confirm_password="weak",
        )
