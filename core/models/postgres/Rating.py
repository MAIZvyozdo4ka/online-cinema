from sqlalchemy.orm import Mapped
from sqlalchemy import DDL, event
from .Movie import MovieDB
from .User import UserDB
from .Base import Base
from .column_types import pk_key_column, cascade_foreign_key, many_to_one_relationship, created_at_type, updated_at_type


class RatingDB(Base):
    
    __tablename__ = 'user_movie_rating'
    
    rating : Mapped[int] 
    movie_id : Mapped[int] = pk_key_column(cascade_foreign_key('movies.id'))
    user_id : Mapped[int] = pk_key_column(cascade_foreign_key('users.id'))
    
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]
    
    user : Mapped[UserDB] = many_to_one_relationship(back_populates = 'user_movies_rating')
    movie : Mapped[MovieDB] = many_to_one_relationship(back_populates = 'movie_rating')
    
    