"""user-add-role

Revision ID: 01e091d36537
Revises: d24cec0c6ddd
Create Date: 2022-01-17 14:35:51.964564

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "01e091d36537"
down_revision = "7b3e0dc2a28e"
branch_labels = None
depends_on = None


userrole_enum = sa.Enum("USER", "ADMIN", name="userrole")


def upgrade():
    userrole_enum.create(op.get_bind(), checkfirst=False)
    op.add_column(
        "user",
        sa.Column("role", userrole_enum, nullable=True, server_default="USER"),
    )
    op.alter_column("user", "role", server_default=None)


def downgrade():
    op.drop_column("user", "role")
    userrole_enum.drop(op.get_bind())
