"""archive + pin

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-19

"""
from alembic import op
import sqlalchemy as sa


revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "notes",
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "notes",
        sa.Column("pinned_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_notes_archived_at", "notes", ["archived_at"])
    op.create_index("ix_notes_pinned_at", "notes", ["pinned_at"])


def downgrade():
    op.drop_index("ix_notes_pinned_at", "notes")
    op.drop_index("ix_notes_archived_at", "notes")
    op.drop_column("notes", "pinned_at")
    op.drop_column("notes", "archived_at")
