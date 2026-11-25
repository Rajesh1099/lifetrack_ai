
"""update users and add refresh tokens

Revision ID: 1606a83a1709
Revises: 43f5b4c3d765
Create Date: 2026-11-25 12:07:00.668274
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '1606a83a1709'
down_revision: Union[str, Sequence[str], None] = '43f5b4c3d765'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=500), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_refresh_tokens_id'),
        'refresh_tokens',
        ['id'],
        unique=False
    )

    op.create_index(
        op.f('ix_refresh_tokens_token'),
        'refresh_tokens',
        ['token'],
        unique=True
    )

    # Add new columns temporarily as nullable
    op.add_column(
        'users',
        sa.Column('first_name', sa.String(100), nullable=True)
    )

    op.add_column(
        'users',
        sa.Column('last_name', sa.String(100), nullable=True)
    )

    op.add_column(
        'users',
        sa.Column('is_verified', sa.Boolean(), nullable=True)
    )

    # Copy existing full_name data
    op.execute("""
        UPDATE users
        SET
            first_name = split_part(trim(full_name), ' ', 1),
            last_name = CASE
                WHEN position(' ' in trim(full_name)) > 0
                THEN trim(substring(
                    trim(full_name)
                    FROM position(' ' in trim(full_name)) + 1
                ))
                ELSE ''
            END,
            is_verified = FALSE
    """)

    # Make new columns mandatory
    op.alter_column(
        'users', 'first_name',
        existing_type=sa.String(100),
        nullable=False
    )

    op.alter_column(
        'users', 'last_name',
        existing_type=sa.String(100),
        nullable=False
    )

    op.alter_column(
        'users', 'is_verified',
        existing_type=sa.Boolean(),
        nullable=False
    )

    # Remove old column after copying its data
    op.drop_column('users', 'full_name')


def downgrade() -> None:

    op.add_column(
        'users',
        sa.Column('full_name', sa.String(100), nullable=True)
    )

    op.execute("""
        UPDATE users
        SET full_name = trim(
            COALESCE(first_name, '') || ' ' || COALESCE(last_name, '')
        )
    """)

    op.alter_column(
        'users', 'full_name',
        existing_type=sa.String(100),
        nullable=False
    )

    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')

    op.drop_index(
        op.f('ix_refresh_tokens_token'),
        table_name='refresh_tokens'
    )

    op.drop_index(
        op.f('ix_refresh_tokens_id'),
        table_name='refresh_tokens'
    )

    op.drop_table('refresh_tokens')
