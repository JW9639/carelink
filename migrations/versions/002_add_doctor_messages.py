"""Add doctor messages.

Revision ID: 002_add_doctor_messages
Revises: 001_initial_schema
Create Date: 2026-01-09 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "002_add_doctor_messages"
down_revision = "001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply migration."""
    op.create_table(
        "doctor_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "doctor_id",
            sa.Integer(),
            sa.ForeignKey("doctors.id"),
            nullable=False,
        ),
        sa.Column("sent_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column(
            "is_read",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_doctor_messages_id", "doctor_messages", ["id"])
    op.create_index(
        "ix_doctor_messages_doctor_id", "doctor_messages", ["doctor_id"]
    )


def downgrade() -> None:
    """Revert migration."""
    op.drop_index("ix_doctor_messages_doctor_id", table_name="doctor_messages")
    op.drop_index("ix_doctor_messages_id", table_name="doctor_messages")
    op.drop_table("doctor_messages")
