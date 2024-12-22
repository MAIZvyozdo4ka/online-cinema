"""add recommendations

Revision ID: 32f9e2f47d61
Revises: 339da7578851
Create Date: 2024-12-15 16:49:26.218236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, array
from migration.TableInit import TableInit


# revision identifiers, used by Alembic.
revision: str = '32f9e2f47d61'
down_revision: Union[str, None] = '339da7578851'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    default_movies = TableInit.get_list_movies_from_file('migration/versions/csv_data/default_rec.csv')
    rec = op.create_table('recommedation',
                    sa.Column('userId', sa.Integer(), nullable=False),
                    sa.Column(
                        'recommedation', ARRAY(sa.Integer()), server_default=array(default_movies), nullable=False
                    ),
                    sa.PrimaryKeyConstraint('userId'),
                    sa.ForeignKeyConstraint(['userId'], ['users.id'], ondelete='CASCADE'),
    )
    TableInit.insert_data_from_file(rec, 'migration/versions/csv_data/users_id.csv', ['userId'])


def downgrade() -> None:
    op.drop_table('recommedation')
