import pytest 
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.postgres.Base import engine
from tests.Base import fixture
from auth_service.app.auth.schemas import UserRegistrationCredentialsIn
from core.dependencies.JWTToken import IssuedJWTTokensOut, TokenValidation
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.app.auth.dao import AuthDAO
from fastapi import Request
from admin_service.app.moive.dao import AdminMovieDAO
from admin_service.app.moive.schemas import NewMovieIn
from tests.Base import MovieType




@fixture(scope = 'function')
async def session():
    async with engine.connect() as connection:
         async with connection.begin() as transaction:
             
            yield AsyncSession(
                bind = connection, join_transaction_mode = 'create_savepoint'
            )

            await transaction.rollback()
    await engine.dispose()
    




@fixture
async def test_user_data() -> dict[str, str]: 
    return {
        'username' : 'test_user_1',
        'first_name' : 'test',
        'last_name' : 'user',
        'email' : 'test_user_email@gmail.com',
        'password' : 'test_user_1'
    }
    


@fixture
async def test_users_data() -> list[dict[str, str]]:
    return [
        {
            'username' : 'test_user_1',
            'first_name' : 'test',
            'last_name' : 'user',
            'email' : 'test_user_email@gmail.com',
            'password' : 'test_user_1'
        },
        {
            'username' : 'test_user_sescond',
            'first_name' : 'second',
            'last_name' : 'second_test',
            'email' : 'second_test_user_email@gmail.com',
            'password' : 'test_user_2'
        },
        {
            'username' : 'test_user_3',
            'first_name' : 'tree',
            'last_name' : 'tree_test',
            'email' : 'tree_test_user_email@gmail.com',
            'password' : 'test_user_3'
        } 
    ]
    
    



@fixture(scope = 'function')
async def user_registrate(session : AsyncSession, test_user_data : dict[str, str]) -> tuple[dict[str, str], IssuedJWTTokensOut]:
    tokens = await AuthDAO.registrate(session, UserRegistrationCredentialsIn.model_validate(test_user_data))
    await session.commit()
    return (test_user_data, tokens)



@fixture(scope = 'function')
async def get_user_request(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> tuple[dict[str, str], int, IssuedJWTTokensOut]:
    req = Request(scope = {'type' : 'http'})
    await TokenValidation.check_accsess_token_with_session(req, f'Bearer {user_registrate[1].access_token}', session)
    
    return user_registrate[0], req.state.user.user_id, user_registrate[1]



@fixture(scope = 'function')
async def movies() -> list[MovieType]:
    return [
        {
            'title' : 'test_movie_title_1',
            'description' : 'test_movie_description_1',
            'genres' : [
                'genre_1', 'genre_2'
            ],
            'links' : {
                'imdb_link' : 'https://www.imdb.com/title/tt1010101',
                'tmbd_link' : 'https://www.themoviedb.org/movie/1010101'
            }
        },
        {
            'title' : 'test_movie_title_2',
            'description' : 'test_movie_description_2',
            'genres' : [
                'genre_1', 'genre_3'
            ],
            'links' : {
                'imdb_link' : 'https://www.imdb.com/title/tt1010102',
                'tmbd_link' : 'https://www.themoviedb.org/movie/1010102'
            }
        },
        {
            'title' : 'test_movie_title_3',
            'description' : 'test_movie_description_3',
            'genres' : [
                'genre_3'
            ],
            'links' : {
                'imdb_link' : 'https://www.imdb.com/title/tt101010',
                'tmbd_link' : 'https://www.themoviedb.org/movie/101010'
            }
        }
    ]
    
    
@fixture(scope = 'function')
async def db_movies(session : AsyncSession, movies : list[MovieType]) -> tuple[list[int], list[MovieType]]:
    ids = []
    for movie in movies:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movie))
        ids.append(movie_id)
        
    return ids, movies


@fixture(scope = 'function')
async def db_users(session : AsyncSession, test_users_data : list[dict[str, str]]) -> tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]]:
    tokens : list[IssuedJWTTokensOut] = []
    ids = []
    for user in test_users_data:
        tokens.append(await AuthDAO.registrate(session, UserRegistrationCredentialsIn.model_validate(user)))
    await session.commit()
    for token in tokens:
        req = Request(scope = {'type' : 'http'})
        await TokenValidation.check_accsess_token_with_session(req, f'Bearer {token.access_token}', session)
        ids.append(req.state.user.user_id)
        
    return test_users_data, ids, tokens