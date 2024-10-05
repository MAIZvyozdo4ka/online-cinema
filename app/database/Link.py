from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .Base import Base



class Link(Base):
    
    __tablename__ = 'links'
    
    id : Mapped[int] = mapped_column(primary_key = True)
    movie_id : Mapped[int] = mapped_column(ForeignKey('movies.movie_id'), unique = True)
    imdb_id : Mapped[int | None] = mapped_column(unique = True)
    tmbd_id : Mapped[int | None] = mapped_column(unique = True)
    movie = relationship('Movie', back_populates = 'link', lazy = 'selectin')
    
    def __repr__(self) -> str:
        return f'Link(id = {self.id}, imdb_id = {self.imdb_id}, tmbd_id = {self.tmbd_id})'