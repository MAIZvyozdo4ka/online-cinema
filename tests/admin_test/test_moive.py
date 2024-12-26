from tests.Base import TestBase, MovieType
from admin_service.app.moive.dao import AdminMovieDAO
from admin_service.app.moive.schemas import NewMovieIn, UpdateMoiveIn, LinksForAnotherSiteIn
from admin_service.app.moive.errors import MovieActionException, MovieActionErrorType
from auth_service.app.auth.errors import AuthException, AuthErrorType
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from core.models.postgres import MovieDB, LinkDB








class TestAdminMovie(TestBase):
    
    
    @staticmethod
    async def test_insert_movie(session : AsyncSession, movies : list[MovieType]) -> None:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        movie = await session.get(MovieDB, movie_id)
        assert movie.title == movies[0]['title']
        assert movie.description == movies[0]['description']
        assert movie.genres == '|'.join(movies[0]['genres'])
        links = await session.get(LinkDB, movie_id)
        assert links.imdb_id == int(movies[0]['links']['imdb_link'].rsplit('/', 1)[1].removeprefix('tt'))
        assert links.tmbd_id == int(movies[0]['links']['tmbd_link'].rsplit('/', 1)[1].removeprefix('tt'))
        
    
    @staticmethod
    async def test_insert_wit_same_title(session : AsyncSession, movies : list[MovieType]) -> None:
        movie2 = movies[1]
        movie2['title'] = movies[0]['title']
        await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        with pytest.raises(MovieActionException) as error:
            await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movie2))
            
        assert error.value.detail['ditail']['type'] == MovieActionErrorType.MOVIE_ALREADY_EXIST
        
        
    @staticmethod
    async def test_insert_wit_same_links(session : AsyncSession, movies : list[MovieType]) -> None:
        movie2 = movies[1]
        movie2['links'] = movies[0]['links']
        await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        with pytest.raises(MovieActionException) as error:
            await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movie2))
            
        assert error.value.detail['ditail']['type'] == MovieActionErrorType.LINK_ALREADY_EXIST  
        
        
    @staticmethod
    async def test_delete_movie(session : AsyncSession, movies : list[MovieType]) -> None:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        await AdminMovieDAO.delete_movie(session, movie_id)
        
        
    @staticmethod
    async def test_delete_movie_with_incorrect_id(session : AsyncSession, movies : list[MovieType]) -> None:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        await AdminMovieDAO.delete_movie(session, movie_id)
        with pytest.raises(MovieActionException) as error:
            await AdminMovieDAO.delete_movie(session, movie_id)
            
        assert error.value.detail['ditail']['type'] == MovieActionErrorType.MOVIE_NOT_FOUND
        
    
      
    @staticmethod
    async def test_delete_movie_with_incorrect_id_2(session : AsyncSession, movies : list[MovieType]) -> None:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        with pytest.raises(MovieActionException) as error:
            await AdminMovieDAO.delete_movie(session, movie_id + 1)
            
        assert error.value.detail['ditail']['type'] == MovieActionErrorType.MOVIE_NOT_FOUND
        
    
    @staticmethod
    async def test_update_title(session : AsyncSession, movies : list[MovieType]) -> None:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        await AdminMovieDAO.update_movie(session, UpdateMoiveIn(title = 'new_test_title', id = movie_id))
        movie = await session.get(MovieDB, movie_id)
        assert movie.title == 'new_test_title'
        assert movie.description == movies[0]['description']
        assert movie.genres == '|'.join(movies[0]['genres'])
        
    
    @staticmethod
    async def test_update_description(session : AsyncSession, movies : list[MovieType]) -> None:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        await AdminMovieDAO.update_movie(session, UpdateMoiveIn(description = 'new_test_description', id = movie_id))
        movie = await session.get(MovieDB, movie_id)
        assert movie.title == movies[0]['title']
        assert movie.description == 'new_test_description'
        assert movie.genres == '|'.join(movies[0]['genres'])
        
        
    @staticmethod
    async def test_update_genres(session : AsyncSession, movies : list[MovieType]) -> None:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        new_genres = ['new_genre_1', 'new_genre_2']
        await AdminMovieDAO.update_movie(session, UpdateMoiveIn(genres = new_genres, id = movie_id))
        movie = await session.get(MovieDB, movie_id)
        assert movie.title == movies[0]['title']
        assert movie.description == movies[0]['description']
        assert movie.genres == '|'.join(new_genres)
        
        
    @staticmethod
    async def test_update_links(session : AsyncSession, movies : list[MovieType]) -> None:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        await AdminMovieDAO.update_movie(session, UpdateMoiveIn(id = movie_id, links = LinksForAnotherSiteIn.model_validate(movies[1]['links'])))
        links = await session.get(LinkDB, movie_id)
        assert links.imdb_id == int(movies[1]['links']['imdb_link'].rsplit('/', 1)[1].removeprefix('tt'))
        assert links.tmbd_id == int(movies[1]['links']['tmbd_link'].rsplit('/', 1)[1].removeprefix('tt'))
        
        
    @staticmethod
    async def test_update_empty(session : AsyncSession, movies : list[MovieType]) -> None:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        with pytest.raises(MovieActionException) as error:
            await AdminMovieDAO.update_movie(session, UpdateMoiveIn(id = movie_id))
            
        assert error.value.detail['ditail']['type'] == MovieActionErrorType.EMPTY_REQUEST
        
      
        
    @staticmethod
    async def test_update_with_same_title(session : AsyncSession, movies : list[MovieType]) -> None:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[1]))
        with pytest.raises(MovieActionException) as error:
            await AdminMovieDAO.update_movie(session, UpdateMoiveIn(id = movie_id, title = movies[1]['title']))
            
        assert error.value.detail['ditail']['type'] == MovieActionErrorType.MOVIE_ALREADY_EXIST
        
        
    @staticmethod
    async def test_update_with_same_links(session : AsyncSession, movies : list[MovieType]) -> None:
        movie_id = await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[0]))
        await AdminMovieDAO.insert_new_movie(session, NewMovieIn.model_validate(movies[1]))
        with pytest.raises(MovieActionException) as error:
            await AdminMovieDAO.update_movie(session, UpdateMoiveIn(id = movie_id, links = LinksForAnotherSiteIn.model_validate(movies[1]['links'])))
            
        assert error.value.detail['ditail']['type'] == MovieActionErrorType.LINK_ALREADY_EXIST
        