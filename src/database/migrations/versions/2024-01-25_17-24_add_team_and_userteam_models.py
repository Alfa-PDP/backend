"""add Team and UserTeam models

Revision ID: 8e68069cf1d2
Revises: b79887e7d53d
Create Date: 2024-01-25 17:24:54.009308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e68069cf1d2'
down_revision: Union[str, None] = 'b79887e7d53d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teams',
    sa.Column('team_name', sa.String(length=100), nullable=False, comment='Наименование команды'),
    sa.Column('leader_id', sa.UUID(), nullable=False, comment='Руководитель команды'),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['leader_id'], ['users.id'], name='teams_leader_fkey', onupdate='RESTRICT', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_teams',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('team_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], name='users_teams_team_id_fkey', onupdate='RESTRICT', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='users_teams_user_id_fkey', onupdate='RESTRICT', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('user_id', 'team_id', name='users_teams_pkey')
    )
    op.add_column('users', sa.Column('middle_name', sa.String(length=50), nullable=False, comment='Отчество пользователя'))
    op.alter_column('users', 'name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=50),
               existing_comment='Имя пользователя',
               existing_nullable=False)
    op.alter_column('users', 'family_name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=50),
               existing_comment='Фамилия пользователя',
               existing_nullable=False)
    op.alter_column('users', 'position',
               existing_type=sa.TEXT(),
               type_=sa.String(length=100),
               existing_comment='Должность пользователя',
               existing_nullable=False)
    op.drop_column('users', 'surname')
    op.drop_column('users', 'role')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.TEXT(), autoincrement=False, nullable=False, comment='Роль пользователя'))
    op.add_column('users', sa.Column('surname', sa.TEXT(), autoincrement=False, nullable=False, comment='Отчество пользователя'))
    op.alter_column('users', 'position',
               existing_type=sa.String(length=100),
               type_=sa.TEXT(),
               existing_comment='Должность пользователя',
               existing_nullable=False)
    op.alter_column('users', 'family_name',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(),
               existing_comment='Фамилия пользователя',
               existing_nullable=False)
    op.alter_column('users', 'name',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(),
               existing_comment='Имя пользователя',
               existing_nullable=False)
    op.drop_column('users', 'middle_name')
    op.drop_table('users_teams')
    op.drop_table('teams')
    # ### end Alembic commands ###
