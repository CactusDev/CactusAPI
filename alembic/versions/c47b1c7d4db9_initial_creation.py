"""Initial creation

Revision ID: c47b1c7d4db9
Revises:
Create Date: 2016-06-11 17:48:59.963968

"""

# revision identifiers, used by Alembic.
revision = 'c47b1c7d4db9'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.String, primary_key=True)
    )

    op.create_table(
        "address",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey('users.id'))
    )


def downgrade():
    op.drop_table("users")
    op.drop_table("address")
