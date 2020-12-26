"""empty message

Revision ID: f534260e3d0a
Revises: b32e21ac69a5
Create Date: 2020-12-26 00:21:06.724399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f534260e3d0a'
down_revision = 'b32e21ac69a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_description', sa.String(length=255), nullable=True))
    op.add_column('artists', sa.Column('seeking_venue', sa.String(), nullable=True))
    op.add_column('artists', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('seeking_description', sa.String(length=255), nullable=True))
    op.add_column('venues', sa.Column('seeking_talent', sa.String(), nullable=True))
    op.add_column('venues', sa.Column('website', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'website')
    op.drop_column('venues', 'seeking_talent')
    op.drop_column('venues', 'seeking_description')
    op.drop_column('artists', 'website')
    op.drop_column('artists', 'seeking_venue')
    op.drop_column('artists', 'seeking_description')
    # ### end Alembic commands ###