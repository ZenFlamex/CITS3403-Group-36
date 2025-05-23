"""Add genre to book

Revision ID: 75955be8f2aa
Revises: 0f1fec7d8e75
Create Date: 2025-04-28 16:43:22.778382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75955be8f2aa'
down_revision = '0f1fec7d8e75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genre', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('genre')

    # ### end Alembic commands ###
