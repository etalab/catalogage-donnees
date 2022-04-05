"""add-dataset-timefields

Revision ID: 6fd05f9d4158
Revises: 67a6c2bf0696
Create Date: 2022-04-05 12:24:18.910412

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6fd05f9d4158"
down_revision = "67a6c2bf0696"
branch_labels = None
depends_on = None


update_frequency_enum = sa.Enum(
    "NEVER",
    "REALTIME",
    "DAILY",
    "WEEKLY",
    "MONTHLY",
    "YEARLY",
    name="update_frequency_enum",
)


def upgrade():
    update_frequency_enum.create(op.get_bind())

    op.add_column(
        "dataset",
        sa.Column("first_published_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "dataset",
        sa.Column("update_frequency", update_frequency_enum, nullable=True),
    )
    op.add_column(
        "dataset",
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_column("dataset", "last_updated_at")
    op.drop_column("dataset", "update_frequency")
    op.drop_column("dataset", "first_published_at")
    update_frequency_enum.drop(op.get_bind())
