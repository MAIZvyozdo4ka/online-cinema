from sqlalchemy.orm import relationship, Mapped, mapped_column, column_property
from .Base import Base
from sqlalchemy.ext.hybrid import hybrid_property
from .column_types import pk_key_identity_column, unique_column, one_to_one_relationship, many_to_many_relationship


class TrainRatingsDB(Base):
    __tablename__ = 'train_ratings'
    user_id: Mapped[int] = pk_key_identity_column()
    movie_id: Mapped[int]
    rating: Mapped[float] = mapped_column(server_default='0')



