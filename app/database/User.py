from sqlalchemy.orm import relationship, Mapped, mapped_column
from .Base import Base
from sqlalchemy import UniqueConstraint


class UserDB(Base):
    
    __tablename__ = 'users'
    
    id : Mapped[int] = mapped_column(primary_key = True)
    username : Mapped[str] = mapped_column(unique = True)
    first_name : Mapped[str]
    last_name : Mapped[str]
    email : Mapped[str] = mapped_column(unique = True)
    is_admin : Mapped[bool] = mapped_column(default = False)
    hash_password : Mapped[str]
    watch_history = relationship('WatchHistoryDB',
                                 back_populates = 'user',
                                 lazy = 'raise_on_sql',
                                 cascade = 'all',
                                 passive_deletes = True
                            )
    
    tokens = relationship('IssuedJWTTokenDB',
                          back_populates = 'subject',
                          lazy = 'raise_on_sql',
                          cascade = 'all',
                          passive_deletes = True
                        )

