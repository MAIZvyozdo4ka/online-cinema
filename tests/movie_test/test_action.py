from tests.Base import TestBase, MovieType
from core.models.postgres import MovieDB, LinkDB
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from movie_service.app.action.dao import MovieDAO
from movie_service.app.action.errors import MovieHTTPException




class TestMovieAction(TestBase):
    
    
    
    @staticmethod
    async def test_get_movie_by_id(session : AsyncSession, db_movies : tuple[list[int], list[MovieType]]) -> None:
        movie_list = []
        for movie_id in db_movies[0]:
            movie_list.append(await MovieDAO.get_movie_by_id(session, movie_id))
            
        for movie_dict, movie_db in zip(db_movies[1], movie_list):
            assert movie_dict['title'] == movie_db.title
            assert movie_dict['genres'] == movie_db.genres
            assert movie_dict['description'] == movie_db.description
            
            
    @staticmethod
    async def test_get_movie_by_incorrect_id(session : AsyncSession, db_movies : tuple[list[int], list[MovieType]]) -> None:
        with pytest.raises(MovieHTTPException) as error:
            await MovieDAO.get_movie_by_id(session, db_movies[0][-1] + 1)
            
        assert error.value.status_code == 404