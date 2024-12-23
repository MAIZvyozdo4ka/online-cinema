"""add training ratings

Revision ID: 339da7578851
Revises: 1f8e1fb41cc8
Create Date: 2024-12-15 16:03:37.712659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from migration.TableInit import TableInit


# revision identifiers, used by Alembic.
revision: str = '339da7578851'
down_revision: Union[str, None] = '1f8e1fb41cc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    ratings = op.create_table('train_ratings',
                              sa.Column('user_id', sa.Integer(), nullable=False),
                              sa.Column('movie_id', sa.Integer(), nullable=False),
                              sa.Column('rating', sa.Float(), server_default='0')
                              )
    TableInit.insert_data_from_file(ratings,
                                    'migration/versions/csv_data/new_clear_rating_small.csv',
                                    ['user_id', 'movie_id', 'rating']
                                    )


def downgrade() -> None:
    op.drop_table('train_ratings')
