from sqlalchemy.orm import relationship, Mapped, mapped_column
from .Base import Base



class User(Base):
    
    __tablename__ = 'users'
    
    id : Mapped[int] = mapped_column(primary_key = True)
    first_name : Mapped[str]
    last_name : Mapped[str]
    email : Mapped[str] = mapped_column(unique = True)
    hash_password : Mapped[str]
    watch_history = relationship('WatchHistory', back_populates = 'user', lazy = 'selectin')
    

