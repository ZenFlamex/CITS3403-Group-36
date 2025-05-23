"""Added join date for users and fixed depreciated datetime for Notification and Bookshare

Revision ID: d1d83f482975
Revises: f38c73fb8af8
Create Date: 2025-05-09 16:06:41.119140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1d83f482975'
down_revision = 'f38c73fb8af8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book_shares', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=False))
        batch_op.drop_column('shared_at')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('join_date', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('join_date')

    with op.batch_alter_table('book_shares', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shared_at', sa.DATETIME(), nullable=False))
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###
