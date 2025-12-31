"""Tests for database session utilities."""

import pytest
from sqlalchemy.orm import Session

from app.db.session import get_db


def test_get_db_yields_session():
    db_gen = get_db()
    db = next(db_gen)
    assert isinstance(db, Session)
    db_gen.close()


def test_get_db_handles_exception():
    db_gen = get_db()
    next(db_gen)
    with pytest.raises(RuntimeError):
        db_gen.throw(RuntimeError("rollback"))
