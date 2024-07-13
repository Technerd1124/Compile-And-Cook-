"""empty message

Revision ID: 72032bcae6a9
Revises: a3cc1f922fd4
Create Date: 2024-07-03 19:34:24.399879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72032bcae6a9'
down_revision = 'a3cc1f922fd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('login', schema=None) as batch_op:
        batch_op.alter_column('phone_no',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('login', schema=None) as batch_op:
        batch_op.alter_column('phone_no',
               existing_type=sa.String(length=20),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###