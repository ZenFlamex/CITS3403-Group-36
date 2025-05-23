"""Add timestamp to reading_progress

Revision ID: 7113bc165fba
Revises: d1d83f482975
Create Date: 2025-05-11 11:19:26.106176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7113bc165fba'
down_revision = 'd1d83f482975'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reading_progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reading_progress', schema=None) as batch_op:
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###
