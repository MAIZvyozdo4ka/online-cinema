from sqlalchemy.orm import relationship, Mapped, mapped_column
from .Base import Base
from sqlalchemy import UUID, func
from uuid import uuid4
from .User import UserDB
from .column_types import pk_key_column, cascade_foreign_key, many_to_one_relationship




class IssuedJWTTokenDB(Base):
    
    __tablename__ = 'issued_jwt_tokens'
    
    jti = pk_key_column(UUID, default = uuid4)
    device_id : Mapped[str] 
    user_id : Mapped[int] = mapped_column(cascade_foreign_key('users.id'))
    subject : Mapped[UserDB] = many_to_one_relationship(back_populates = 'tokens')
    