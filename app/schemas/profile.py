"""Profile and credential schemas."""

from __future__ import annotations

from pydantic import BaseModel, model_validator

from app.utils.validators import validate_password_strength


class PatientProfileUpdate(BaseModel):
    """Editable patient fields."""

    phone_number: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    postcode: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_relationship: str | None = None
    emergency_contact_phone: str | None = None
    doctor_id: int | None = None


class DoctorProfileUpdate(BaseModel):
    """Editable doctor fields."""

    title: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    specialty: str | None = None
    phone_number: str | None = None
    email: str | None = None


class PasswordChange(BaseModel):
    """Password change payload."""

    current_password: str
    new_password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self) -> "PasswordChange":
        """Ensure new password and confirmation match and are strong."""
        if self.new_password != self.confirm_password:
            msg = "New password and confirmation must match."
            raise ValueError(msg)

        is_valid, error = validate_password_strength(self.new_password)
        if not is_valid:
            raise ValueError(error)
        return self
