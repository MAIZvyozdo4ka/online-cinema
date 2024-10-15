from sqlalchemy.orm import relationship, Mapped, mapped_column
from .Base import Base
from sqlalchemy import ForeignKey, func
from datetime import datetime
from .User import UserDB




class WatchHistoryDB(Base):
    
    __tablename__ = 'users_watch_history'
    
    id : Mapped[int] = mapped_column(primary_key = True)
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id', ondelete = 'CASCADE'))
    created_at : Mapped[datetime] = mapped_column(server_default = func.now())
    text : Mapped[str] 
    user : Mapped[UserDB] = relationship(back_populates = 'watch_history',
                                         lazy = 'raise_on_sql',
                                         uselist = False
                                        )
    
    
