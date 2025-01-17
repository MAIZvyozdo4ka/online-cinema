"""admin

Revision ID: 1f8e1fb41cc8
Revises: b043524c6349
Create Date: 2024-12-02 05:40:34.448987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from migration.TableInit import TableInit, DatabaseRandomRowsGenrator

# revision identifiers, used by Alembic.
revision: str = '1f8e1fb41cc8'
down_revision: Union[str, None] = 'b043524c6349'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    users = sa.Table('users', sa.MetaData(), autoload_with = op.get_bind())
    TableInit.insert_data_from_file(users, 'migration/versions/csv_data/admin.csv', ['id','role', 'first_name', 'last_name', 'username', 'email', 'hash_password'], [0])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    ids = DatabaseRandomRowsGenrator.get_ids('migration/versions/csv_data/admin.csv')
    users = sa.Table('users', sa.MetaData(), autoload_with = op.get_bind())
    op.execute(users.delete().where(users.c.id.in_(ids)))
    # ### end Alembic commands ###
