from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from config import get_db_url



DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL, echo = False) 
async_session_maker = async_sessionmaker(engine)



class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True