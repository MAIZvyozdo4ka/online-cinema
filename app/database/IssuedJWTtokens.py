from sqlalchemy.orm import relationship, Mapped, mapped_column
from .Base import Base
from sqlalchemy import ForeignKey, UUID
from uuid import uuid4
from .User import UserDB




class IssuedJWTTokenDB(Base):
    
    __tablename__ = 'issued_jwt_tokens'
    
    jti = mapped_column(UUID, primary_key = True)
    device_id : Mapped[str] 
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id', ondelete = 'CASCADE'))
    subject : Mapped[UserDB] = relationship(back_populates = 'tokens',
                                            lazy = 'selectin',
                                            uselist = False
                                        )
    