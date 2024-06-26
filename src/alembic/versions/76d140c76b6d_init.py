"""init

Revision ID: 76d140c76b6d
Revises: 2fd68d167836
Create Date: 2024-06-21 13:56:40.031658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76d140c76b6d'
down_revision: Union[str, None] = '2fd68d167836'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('interfaces', sa.Column('name', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('interfaces', 'name')
    # ### end Alembic commands ###
