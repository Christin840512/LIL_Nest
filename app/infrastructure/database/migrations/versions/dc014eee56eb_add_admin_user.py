"""add admin user

Revision ID: dc014eee56eb
Revises: 84f049308195
Create Date: 2025-12-21 14:20:21.061724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.infrastructure.external.security.password_hasher import _pwd_ctx
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = 'dc014eee56eb'
down_revision: Union[str, Sequence[str], None] = '84f049308195'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        sa.text(
            """
            INSERT INTO users (id, username, password_hash, last_login_at)
            VALUES (1, 'admin', :password_hash, NULL)
            """
        ).bindparams(password_hash=_pwd_ctx.hash("admin123"))
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            """
            DELETE FROM users WHERE id = 1
            """
        )
    )   