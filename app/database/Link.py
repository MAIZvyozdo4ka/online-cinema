from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .Base import Base
from .column_types import cascade_foreign_key, pk_key_column, unique_column



class LinkDB(Base):
    
    __tablename__ = 'links'
    
    movie_id : Mapped[int] = pk_key_column(cascade_foreign_key('movies.id'))
    imdb_id : Mapped[int | None] = unique_column()
    tmbd_id : Mapped[int | None] = unique_column()
    