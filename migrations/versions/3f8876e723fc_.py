"""empty message

Revision ID: 3f8876e723fc
Revises: 95ca2471f534
Create Date: 2023-03-01 15:30:44.245423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f8876e723fc'
down_revision = '95ca2471f534'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'bikes', ['number'])
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('users', 'surname',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('users', 'birth_day',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'birth_day',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('users', 'surname',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.drop_constraint(None, 'bikes', type_='unique')
    # ### end Alembic commands ###
