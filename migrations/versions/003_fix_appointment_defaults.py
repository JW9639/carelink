"""Fix appointment defaults and nullable doctor assignments.

Revision ID: 003_fix_appointment_defaults
Revises: 002_add_pending_status
Create Date: 2026-01-07 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "003_fix_appointment_defaults"
down_revision = "002_add_pending_status"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply appointment default and nullability fixes."""
    op.alter_column(
        "appointments",
        "doctor_id",
        existing_type=sa.Integer(),
        nullable=True,
    )
    op.alter_column(
        "appointments",
        "status",
        existing_type=postgresql.ENUM(
            "scheduled",
            "completed",
            "cancelled",
            "no_show",
            "pending",
            name="appointmentstatus",
            create_type=False,
        ),
        server_default=sa.text("'pending'"),
    )
    op.alter_column(
        "appointments",
        "duration_minutes",
        existing_type=sa.Integer(),
        server_default=sa.text("30"),
    )


def downgrade() -> None:
    """Revert appointment default and nullability fixes."""
    op.alter_column(
        "appointments",
        "duration_minutes",
        existing_type=sa.Integer(),
        server_default=sa.text("15"),
    )
    op.alter_column(
        "appointments",
        "status",
        existing_type=postgresql.ENUM(
            "scheduled",
            "completed",
            "cancelled",
            "no_show",
            "pending",
            name="appointmentstatus",
            create_type=False,
        ),
        server_default=sa.text("'scheduled'"),
    )
    op.alter_column(
        "appointments",
        "doctor_id",
        existing_type=sa.Integer(),
        nullable=False,
    )
