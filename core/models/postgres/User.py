from sqlalchemy.orm import relationship, Mapped, mapped_column
from .Base import Base
from sqlalchemy.ext.hybrid import hybrid_property
from .column_types import pk_key_identity_column, unique_column, one_to_many_relationship, many_to_many_relationship
from enum import StrEnum, auto




class UserRole(StrEnum):
    admin = auto()
    moderator = auto()
    user = auto()
    
    

class UserDB(Base):

    __tablename__ = 'users'
  
    id : Mapped[int] = pk_key_identity_column()
    first_name : Mapped[str]    
    last_name : Mapped[str]
    username : Mapped[str] = unique_column()
    email : Mapped[str] = unique_column()
    role : Mapped[UserRole] = mapped_column(server_default = 'user')
    hash_password : Mapped[str]
  
    tokens = one_to_many_relationship('IssuedJWTTokenDB', back_populates = 'subject')
    user_movies_rating = many_to_many_relationship('RatingDB', back_populates = 'user')
    user_movies_review = many_to_many_relationship('ReviewDB', back_populates = 'user')
  
    @hybrid_property
    def user_movies_rating_count(self) -> int | None:
        if self.__dict__.get('user_movies_rating') is None:
            return None
        
        return len(self.user_movies_rating)
    
    @hybrid_property
    def user_movies_review_count(self) -> int | None:
        if self.__dict__.get('user_movies_review') is None:
            return None
        
        return len(self.user_movies_review)
