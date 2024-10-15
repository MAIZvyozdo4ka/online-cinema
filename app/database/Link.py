from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .Base import Base
from .Movie import MovieDB



class LinkDB(Base):
    
    __tablename__ = 'links'
    
    id : Mapped[int] = mapped_column(primary_key = True)
    movie_id : Mapped[int] = mapped_column(ForeignKey('movies.movie_id', ondelete = 'CASCADE'), unique = True)
    imdb_id : Mapped[int | None] = mapped_column(unique = True)
    tmbd_id : Mapped[int | None] = mapped_column(unique = True)
    
    movie : Mapped[MovieDB] = relationship(back_populates = 'link', 
                                           lazy = 'selectin'
                                        )