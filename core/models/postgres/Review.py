from sqlalchemy.orm import Mapped, mapped_column
from .Movie import MovieDB
from .User import UserDB
from .Base import Base
from .column_types import pk_key_column, cascade_foreign_key, many_to_one_relationship, created_at_type, updated_at_type
from enum import StrEnum, auto




class StatementReviewType(StrEnum):
    positive = auto()
    negative = auto()
    neutral = auto()


class ReviewDB(Base):
    
    __tablename__ = 'user_review_movies'
    
    movie_id : Mapped[int] = pk_key_column(cascade_foreign_key('movies.id'))
    user_id : Mapped[int] = pk_key_column(cascade_foreign_key('users.id'))
    
    header : Mapped[str]
    review : Mapped[str]
    statement : Mapped[StatementReviewType]
    
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]
    
    user : Mapped[UserDB] = many_to_one_relationship(back_populates = 'user_movies_review')
    movie : Mapped[MovieDB] = many_to_one_relationship(back_populates = 'movie_reviews')
    
    
    