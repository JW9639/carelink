"""User schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from app.utils.constants import UserRole


class UserBase(BaseModel):
    """Shared user fields."""

    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    """Payload for creating a user."""

    password: str

    @field_validator("password")
    @classmethod
    def password_length(cls, value: str) -> str:
        """Validate password length."""
        if len(value) < 8:
            msg = "Password must be at least 8 characters long."
            raise ValueError(msg)
        return value


class UserResponse(UserBase):
    """Response model for user data."""

    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Login payload."""

    email: EmailStr
    password: str
