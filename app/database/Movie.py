from sqlalchemy.orm import relationship, Mapped, mapped_column
from .Base import Base



class Movie(Base):
    
    __tablename__ = 'movies'

    movie_id : Mapped[int] = mapped_column(primary_key = True)
    title : Mapped[str] = mapped_column(unique = True)
    genres : Mapped[str]    
    link = relationship('Link', back_populates = 'movie', lazy = 'selectin')
    
    def __repr__(self) -> str:
        return f'Movie(movie_id = {self.movie_id}, title = {self.title}, genres = {self.genres})'



