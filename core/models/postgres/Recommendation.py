from sqlalchemy.orm import relationship, Mapped, mapped_column, column_property
from .Base import Base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Integer, Column
from typing import List
from sqlalchemy.ext.hybrid import hybrid_property
from .column_types import pk_key_identity_column, one_to_one_relationship, pk_key_column, cascade_foreign_key


class RecommedationDB(Base):
    __tablename__ = 'recommedation'

    userId: Mapped[int] = pk_key_column(cascade_foreign_key('users.id'))
    recommedation: Mapped[List[int]] = Column(ARRAY(Integer))


    users = one_to_one_relationship('UserDB')
