"""Add reading_progress table

Revision ID: 475ba5b98cca
Revises: 0d19d5562fec
Create Date: 2025-05-01 11:11:35.721467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '475ba5b98cca'
down_revision = '0d19d5562fec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reading_progress', schema=None) as batch_op:
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reading_progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DATETIME(), nullable=False))

    # ### end Alembic commands ###
