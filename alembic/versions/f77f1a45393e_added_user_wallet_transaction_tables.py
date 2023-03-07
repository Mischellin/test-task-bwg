"""Added user wallet transaction tables

Revision ID: f77f1a45393e
Revises: 
Create Date: 2023-03-07 19:07:41.929297
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "f77f1a45393e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_data",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_table(
        "wallet_data",
        sa.Column("wallet_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("balance", sa.Numeric(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user_data.user_id"],
        ),
        sa.PrimaryKeyConstraint("wallet_id"),
    )
    op.create_table(
        "transaction_data",
        sa.Column("transaction_id", sa.Numeric(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("wallet_id", sa.Integer(), nullable=True),
        sa.Column("ammount", sa.Numeric(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user_data.user_id"],
        ),
        sa.ForeignKeyConstraint(
            ["wallet_id"],
            ["wallet_data.wallet_id"],
        ),
        sa.PrimaryKeyConstraint("transaction_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transaction_data")
    op.drop_table("wallet_data")
    op.drop_table("user_data")
    # ### end Alembic commands ###
