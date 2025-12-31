"""Validation helpers for domain-specific data."""

from __future__ import annotations

import re
from typing import Tuple


def validate_nhs_number(nhs_number: str) -> bool:
    """Validate a 10-digit NHS number using checksum rules."""
    digits = re.sub(r"\D", "", nhs_number)
    if len(digits) != 10:
        return False

    weights = list(range(10, 1, -1))
    total = sum(int(d) * w for d, w in zip(digits[:9], weights))
    remainder = total % 11
    check_digit = (11 - remainder) % 11
    if check_digit == 10:
        return False
    return check_digit == int(digits[-1])


def validate_ni_postcode(postcode: str) -> bool:
    """Validate a Northern Ireland postcode (BT prefix)."""
    normalized = postcode.replace(" ", "").strip().upper()
    pattern = r"^BT\d{1,2}[A-Z]{2}$"
    return bool(re.match(pattern, normalized))


def validate_uk_phone(phone: str) -> bool:
    """Validate UK phone number formats."""
    normalized = re.sub(r"[ \-()\t]", "", phone)
    pattern = r"^(?:\+44|0)\d{10}$"
    return bool(re.match(pattern, normalized))


def validate_gmc_number(gmc_number: str) -> bool:
    """Validate GMC number (7 digits)."""
    return bool(re.match(r"^\d{7}$", gmc_number.strip()))


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Check password strength and return (is_valid, error_message)."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must include an uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must include a lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must include a number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\[\]\\/;+='`~]", password):
        return False, "Password must include a special character."
    return True, ""
