import pytest 
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.Base import engine
from tests.Base import fixture
from sqlalchemy import insert, select
from app.database import UserDB, MovieDB


@fixture(scope = 'function')
async def session():
    async with engine.connect() as connection:
         async with connection.begin() as transaction:
             
            yield AsyncSession(
                bind = connection, join_transaction_mode = 'create_savepoint'
            )

            await transaction.rollback()
    await engine.dispose()
    


@fixture(scope = 'function')
async def add_users(session : AsyncSession) -> list[int]:
    users = [
        {
            'username' : 'test_user_1',
            'first_name' : 'Bob',
            'last_name' : 'Fish',
            'email' : 'bobfish@gmail.com',
            'hash_password' : '12345678',
        },
        {
            'username' : 'test_user_2',
            'first_name' : 'alex',
            'last_name' : 'dude',
            'email' : 'alex197@gmail.com',
            'hash_password' : '2sss',
        },
         {
            'username' : 'test_user_3',
            'first_name' : 'Bim',
            'last_name' : 'BimBim',
            'email' : 'BimBimBimBim@gmail.com',
            'hash_password' : 'waseftcxesdes',
        }
    ]
    insertion = await session.scalars(insert(UserDB).values(users).returning(UserDB.id))
    await session.commit()
    return insertion.all()


@fixture(scope = 'function')
async def add_movies(session : AsyncSession) -> list[int]:
    return [5, 8, 10]


@fixture(scope = 'function')
async def movies(session : AsyncSession, add_movies : list[int]) -> list[int]:
    movies_ = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
    return movies_.all()