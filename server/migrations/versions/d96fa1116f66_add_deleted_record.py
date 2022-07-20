"""add-deleted_record

Revision ID: d96fa1116f66
Revises: d9ea6ea6708f
Create Date: 2022-07-20 13:14:31.542990

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d96fa1116f66"
down_revision = "d9ea6ea6708f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "deleted_record",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            nullable=False,
        ),
        sa.Column("original_table", sa.String(), nullable=False),
        sa.Column(
            "original_pk", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("deleted_record")
