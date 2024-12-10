from sqlalchemy.orm import relationship, Mapped, mapped_column, column_property
from .Base import Base
from sqlalchemy.ext.hybrid import hybrid_property
from .column_types import pk_key_identity_column, unique_column, one_to_one_relationship, many_to_many_relationship



class MovieDB(Base):
    
    __tablename__ = 'movies'

    id : Mapped[int] = pk_key_identity_column()
    title : Mapped[str] = unique_column()
    movie_rating_count : Mapped[int] = mapped_column(server_default = '0') 
    movie_rating_sum : Mapped[int] = mapped_column(server_default = '0')
    movie_reviews_count : Mapped[int] = mapped_column(server_default = '0')
    genres : Mapped[str]
    description : Mapped[str]
    
    link = one_to_one_relationship('LinkDB')
    movie_rating = many_to_many_relationship('RatingDB', back_populates = 'movie')
    movie_reviews = many_to_many_relationship('ReviewDB', back_populates = 'movie')

    @hybrid_property
    def movie_rating_avg(self) -> float:
        if self.movie_rating_count == 0:
            return self.movie_rating_sum
        
        return self.movie_rating_sum / self.movie_rating_count
    
    
    