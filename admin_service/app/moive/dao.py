from .schemas import NewMovieIn, UpdateMoiveIn
from core.models.postgres import MovieDB, LinkDB
from core.dao import PostgresDAO, AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from .errors import MovieAlreadyExistError, LinksAlreadyExistError, MovieNoFoundError, EmptyRequestError
import asyncio



class AdminMovieDAO(PostgresDAO):
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def insert_new_movie(cls, session : AsyncSession, movie : NewMovieIn) -> int:
        try:
            query_for_insert_new_movie = insert(MovieDB).values(movie.model_dump()).returning(MovieDB.id)
            movie_id = await session.scalar(query_for_insert_new_movie)
        except IntegrityError:
            raise MovieAlreadyExistError

        try:
            query_for_insert_new_links = insert(LinkDB).values(**movie.links.model_dump(), movie_id = movie_id)
            await session.execute(query_for_insert_new_links)
        except IntegrityError:
            raise LinksAlreadyExistError
        
        return movie_id
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def update_movie(cls, session : AsyncSession, movie : UpdateMoiveIn) -> None:
        movie_db = await session.get(MovieDB, movie.id)
        movie_dump = movie.model_dump(exclude_none = True)
        
        if movie_db is None:
            raise MovieNoFoundError
        
        if len(movie_dump) == 0 and movie.links is None:
            raise EmptyRequestError
        
        if len(movie_dump) > 0:
            try:
                query_for_update_movie = update(MovieDB).where(MovieDB.id == movie.id).values(movie_dump)
                await session.execute(query_for_update_movie)
            except IntegrityError:
                raise MovieAlreadyExistError
        
        if movie.links is not None:
            
            try:
                query_for_update_links = update(LinkDB).where(LinkDB.movie_id == movie.id).values(movie.links.model_dump())
                await session.execute(query_for_update_links)
            except IntegrityError:
                raise LinksAlreadyExistError
        
     
    @classmethod   
    @PostgresDAO.get_session(auto_commit = True)
    async def delete_movie(cls, session : AsyncSession, movie_id : int) -> None:
        query_for_delete_movie = delete(MovieDB).where(MovieDB.id == movie_id).returning(MovieDB.id)
        query_for_delete_links = delete(LinkDB).where(LinkDB.movie_id == movie_id)
        
        movie_id_db = await session.scalar(query_for_delete_movie)
        
        if movie_id_db is None:
            raise MovieNoFoundError
        
        await session.execute(query_for_delete_links)