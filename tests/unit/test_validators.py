"""Tests for validator helpers."""

from app.utils.validators import (
    validate_gmc_number,
    validate_ni_postcode,
    validate_nhs_number,
    validate_password_strength,
    validate_uk_phone,
)


def test_validate_nhs_number_valid():
    assert validate_nhs_number("943 476 5919")


def test_validate_nhs_number_invalid():
    assert not validate_nhs_number("1234567890")


def test_validate_ni_postcode_valid():
    assert validate_ni_postcode("BT12AB")
    assert validate_ni_postcode("bt1 2ab") is True


def test_validate_ni_postcode_invalid():
    assert not validate_ni_postcode("SW1A1AA")


def test_validate_uk_phone_formats():
    assert validate_uk_phone("07123456789")
    assert validate_uk_phone("+447123456789")
    assert not validate_uk_phone("12345")


def test_validate_password_strength():
    is_valid, _ = validate_password_strength("StrongPass1!")
    assert is_valid
    is_valid, error = validate_password_strength("weak")
    assert not is_valid
    assert error


def test_validate_gmc_number():
    assert validate_gmc_number("1234567")
    assert not validate_gmc_number("ABC1234")
