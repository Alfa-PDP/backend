"""init migration

Revision ID: b79887e7d53d
Revises: 
Create Date: 2024-01-18 22:43:38.839409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b79887e7d53d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('name', sa.Text(), nullable=False, comment='Имя пользователя'),
    sa.Column('family_name', sa.Text(), nullable=False, comment='Фамилия пользователя'),
    sa.Column('surname', sa.Text(), nullable=False, comment='Отчество пользователя'),
    sa.Column('position', sa.Text(), nullable=False, comment='Должность пользователя'),
    sa.Column('role', sa.Text(), nullable=False, comment='Роль пользователя'),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###