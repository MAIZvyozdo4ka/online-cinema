"""add random ratings

Revision ID: b2e3b229115b
Revises: c63b42abf1d7
Create Date: 2024-11-20 00:03:48.279243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from migration.TableInit import TableInit

# revision identifiers, used by Alembic.
revision: str = 'b2e3b229115b'
down_revision: Union[str, None] = 'c63b42abf1d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_movie_rating', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('user_movie_rating', sa.Column('updated_at', sa.DateTime(), onupdate=sa.text('now()'), server_default=sa.text('now()'), nullable=False))
    rating = sa.Table('user_movie_rating', sa.MetaData(), autoload_with = op.get_bind())
    TableInit.insert_data_from_file(rating, 'migration/versions/csv_data/user_ratings.csv', ['rating', 'movie_id', 'user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    rating = sa.Table('user_movie_rating', sa.MetaData(), autoload_with = op.get_bind())
    op.execute(rating.delete())
    op.drop_column('user_movie_rating', 'updated_at')
    op.drop_column('user_movie_rating', 'created_at')
    # ### end Alembic commands ###
