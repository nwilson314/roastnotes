"""add roasters table

Revision ID: 9d827f14a4fd
Revises: 1c1531a1c138
Create Date: 2025-02-12 22:35:49.684785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9d827f14a4fd'
down_revision: Union[str, None] = '1c1531a1c138'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roaster',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('location', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('website', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('social_media', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roaster_name'), 'roaster', ['name'], unique=False)
    op.add_column('roast', sa.Column('roaster_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'roast', 'roaster', ['roaster_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'roast', type_='foreignkey')
    op.drop_column('roast', 'roaster_id')
    op.drop_index(op.f('ix_roaster_name'), table_name='roaster')
    op.drop_table('roaster')
    # ### end Alembic commands ###
