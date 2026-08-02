"""merge heads

Revision ID: 8e5db300ef8c
Revises: b81ca4d353ec, fd8fe76442f7
Create Date: 2026-08-02 11:09:54.145556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e5db300ef8c'
down_revision = ('b81ca4d353ec', 'fd8fe76442f7')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
