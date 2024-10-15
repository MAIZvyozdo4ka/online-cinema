from sqlalchemy.orm import relationship, Mapped, mapped_column
from .Base import Base



class MovieDB(Base):
    
    __tablename__ = 'movies'

    movie_id : Mapped[int] = mapped_column(primary_key = True)
    title : Mapped[str] = mapped_column(unique = True)
    genres : Mapped[str]    
    link = relationship('LinkDB',
                        back_populates = 'movie',
                        lazy = 'selectin',
                        cascade = 'all',
                        uselist = False
                    )
    


