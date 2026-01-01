"""Add pending status to appointment status enum.

Revision ID: 002_add_pending_status
Revises: 001_initial_schema
Create Date: 2026-01-01 00:00:00
"""

from __future__ import annotations

from alembic import op


revision = "002_add_pending_status"
down_revision = "001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add PENDING to appointmentstatus enum."""
    # Add new value to the enum type
    op.execute("ALTER TYPE appointmentstatus ADD VALUE IF NOT EXISTS 'pending'")


def downgrade() -> None:
    """Remove PENDING from appointmentstatus enum.
    
    Note: PostgreSQL doesn't support removing enum values directly.
    This would require recreating the enum type and updating all columns.
    For simplicity, we leave this as a no-op.
    """
    pass
