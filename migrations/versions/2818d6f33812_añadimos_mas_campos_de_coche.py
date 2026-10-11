"""Añadimos mas campos de coche

Revision ID: 2818d6f33812
Revises: da6396043321
Create Date: 2026-10-10 16:29:46.835403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2818d6f33812'
down_revision = 'da6396043321'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'gasoline',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    with op.batch_alter_table('coches', schema=None) as batch_op:
        batch_op.add_column(sa.Column('km', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('cv', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('price', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('place', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('gasoline_type_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_coches_gasoline_type_id_gasoline',
            'gasoline',
            ['gasoline_type_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('coches', schema=None) as batch_op:
        batch_op.drop_constraint('fk_coches_gasoline_type_id_gasoline', type_='foreignkey')
        batch_op.drop_column('gasoline_type_id')
        batch_op.drop_column('place')
        batch_op.drop_column('price')
        batch_op.drop_column('cv')
        batch_op.drop_column('km')

    op.drop_table('gasoline')
