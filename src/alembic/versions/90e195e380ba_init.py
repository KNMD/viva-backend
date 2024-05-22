"""init

Revision ID: 90e195e380ba
Revises: fd774c49809e
Create Date: 2024-05-22 22:46:49.434625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90e195e380ba'
down_revision: Union[str, None] = 'fd774c49809e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('model', sa.Column('context_window', sa.Integer(), nullable=False))
    op.add_column('model', sa.Column('support_vision', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('model', 'support_vision')
    op.drop_column('model', 'context_window')
    # ### end Alembic commands ###