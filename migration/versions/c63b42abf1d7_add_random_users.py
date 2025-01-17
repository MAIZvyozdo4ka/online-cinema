"""add random users

Revision ID: c63b42abf1d7
Revises: d3b64103f556
Create Date: 2024-11-18 23:53:08.830977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from migration.TableInit import TableInit


# revision identifiers, used by Alembic.
revision: str = 'c63b42abf1d7'
down_revision: Union[str, None] = 'd3b64103f556'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    users = sa.Table('users', sa.MetaData(), autoload_with = op.get_bind())
    TableInit.insert_data_from_file(users, 'migration/versions/csv_data/users_clear.csv', ['id', 'username', 'first_name', 'last_name', 'email', 'hash_password'], [0])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    users = sa.Table('users', sa.MetaData(), autoload_with = op.get_bind())
    op.execute(users.delete())
    # ### end Alembic commands ###
