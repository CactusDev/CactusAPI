"""Updating DB to Cube's stat

Revision ID: c689a5475717
Revises: c47b1c7d4db9
Create Date: 2016-06-11 20:25:10.277757

"""

# revision identifiers, used by Alembic.
revision = 'c689a5475717'
down_revision = 'c47b1c7d4db9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table("users")
    op.drop_table("address")

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("userName", sa.String),
        sa.Column("userLevel", sa.Integer),
        sa.Column("enabled", sa.Boolean, default=True),
        sa.Column("botUsername", sa.String),
        sa.Column("botPassword", sa.String)
    )

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("channelId", sa.String),
        sa.Column("userId", sa.String),
        sa.Column("userLevel", sa.Integer),
        sa.Column("createdAt", sa.DateTime)
    )

    op.create_table(
        "channels",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("userId", sa.String, sa.ForeignKey("users.id")),
        sa.Column("enabled", sa.Boolean, default=True),
        sa.Column("createdAt", sa.DateTime),
        sa.Column("service", sa.String)
    )

    op.create_table(
        "configuration",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("channelId", sa.String),
        sa.Column("key", sa.String),
        sa.Column("value", sa.String),
        sa.Column("lastUpdated", sa.String)
    )

    op.create_table(
        "commands",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String),
        sa.Column("response", sa.String),
        sa.Column("enabled", sa.Boolean, default=True),
        sa.Column("deleted", sa.Boolean, default=False),
        sa.Column("channelId", sa.String),
        sa.Column("userLevel", sa.Integer),
        sa.Column("createdAt", sa.DateTime),
        sa.Column("userId", sa.String),
        sa.Column("syntax", sa.String),
        sa.Column("help", sa.String),
        sa.Column("builtIn", sa.Boolean, default=False)
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("message", sa.String),
        sa.Column("channelId", sa.String),
        sa.Column("userId", sa.String),
        sa.Column("createdAt", sa.DateTime)
    )

    op.create_table(
        "executions",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("commandId", sa.String),
        sa.Column("messageId", sa.String)
    )

    op.create_table(
        "quotes",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("quoteId", sa.Integer),
        sa.Column("messageId", sa.String),
        sa.Column("channelId", sa.String),
        sa.Column("userId", sa.String),
        sa.Column("createdAt", sa.DateTime),
        sa.Column("enabled", sa.Boolean, default=True),
        sa.Column("deleted", sa.Boolean, default=False)
    )


def downgrade():
    op.drop_table("users")
    op.drop_table("roles")
    op.drop_table("channels")
    op.drop_table("configuration")
    op.drop_table("commands")
    op.drop_table("messages")
    op.drop_table("executions")
    op.drop_table("quotes")
