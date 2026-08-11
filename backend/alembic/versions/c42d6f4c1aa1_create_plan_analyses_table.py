"""create plan analyses table

Revision ID: c42d6f4c1aa1
Revises: 9b7c9ef73054
Create Date: 2026-08-11 12:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "c42d6f4c1aa1"
down_revision: str | Sequence[str] | None = "9b7c9ef73054"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    analysis_status = sa.Enum(
        "processing",
        "completed",
        "failed",
        name="analysis_status",
    )
    op.create_table(
        "plan_analyses",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("status", analysis_status, nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=False),
        sa.Column("prompt_version", sa.String(length=50), nullable=False),
        sa.Column("result", sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["plan_id"], ["plans.id"], name=op.f("fk_plan_analyses_plan_id_plans"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_plan_analyses")),
    )
    op.create_index(op.f("ix_plan_analyses_plan_id"), "plan_analyses", ["plan_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_plan_analyses_plan_id"), table_name="plan_analyses")
    op.drop_table("plan_analyses")
    sa.Enum(name="analysis_status").drop(op.get_bind(), checkfirst=True)
