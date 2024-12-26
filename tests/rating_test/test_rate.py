from tests.Base import TestBase, MovieType
from core.models.postgres import MovieDB
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from rating_service.app.rate.dao import RatingDAO
from rating_service.app.rate.errors import RatingException, RateErrorType
from rating_service.app.rate.schemas import RateMovieIn, DeleteRateMovieIn
from core.dependencies.JWTToken import IssuedJWTTokensOut
from core.models.postgres import MovieDB






class TestRate(TestBase):
    
    
    
    @staticmethod
    async def test_users_rate(session : AsyncSession,
                              db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                              db_movies : tuple[list[int], list[MovieType]]
                            ) -> None:
        rating_list = [10, 10, 5]
        movie_id = db_movies[0][0]
        for user_id, rating in zip(db_users[1], rating_list):
            model = RateMovieIn(rating = rating, movie_id = movie_id)
            model._user_id = user_id
            await RatingDAO.rate_movie(model, session = session)
            await session.commit()
        
        movie = await session.get(MovieDB, movie_id)
        assert movie.movie_rating_count == len(db_users[1])
        assert movie.movie_rating_sum == sum(rating_list)
        
        
    @staticmethod
    async def test_user_single_rate(
                            session : AsyncSession,
                              db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                              db_movies : tuple[list[int], list[MovieType]]
                            ) -> None:
    
        rating_list = [10, 10, 5, 10, 7]
        movie_id = db_movies[0][0]
        user_id = db_users[1][0]
        for rating in rating_list:
            model = RateMovieIn(rating = rating, movie_id = movie_id)
            model._user_id = user_id
            await RatingDAO.rate_movie(model, session = session)
            await session.commit()
        
        movie = await session.get(MovieDB, movie_id)
        assert movie.movie_rating_count == 1
        assert movie.movie_rating_sum == rating_list[-1]
        
        
    @staticmethod
    async def test_users_rate_with_incorrect_movie_id(session : AsyncSession,
                                                      db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                                      db_movies : tuple[list[int], list[MovieType]]
                                                    ) -> None:
        movie_id = db_movies[0][-1] + 1
        with pytest.raises(RatingException) as error:
            model = RateMovieIn(rating = 10, movie_id = movie_id)
            model._user_id = db_users[1][0]
            await RatingDAO.rate_movie(model, session = session)
            await session.commit()
            
        assert error.value.detail['ditail']['type'] == RateErrorType.MOVIE_NOT_FOUND
     
        
        
    @staticmethod
    async def test_user_view_rate(session : AsyncSession,
                                  db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                  db_movies : tuple[list[int], list[MovieType]]
                                ) -> None:
        rating_list = [10, 4, 8]
        user_id = db_users[1][0]
        for movie_id, rating in zip(db_movies[0], rating_list):
            model = RateMovieIn(rating = rating, movie_id = movie_id)
            model._user_id = user_id
            await RatingDAO.rate_movie(model, session = session)
            await session.commit()
        user_rating = await RatingDAO.get_user_movies_rating(session, user_id)
        assert user_rating.rating_count == len(rating_list)
        for db_rate, rate, movie in zip(user_rating.rate_list, rating_list, db_movies[1]):
            assert db_rate.movie.title == movie['title']
            assert db_rate.rating == rate
            
    
    @staticmethod
    async def test_user_view_empty_rate(session : AsyncSession,
                                        db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                        db_movies : tuple[list[int], list[MovieType]]
                                        ) -> None:
        user_id = db_users[1][0]
        user_rating = await RatingDAO.get_user_movies_rating(session, user_id)
        assert user_rating.rating_count == 0
        assert user_rating.rate_list == []
        
        
        
    @staticmethod
    async def test_users_rate_delete(session : AsyncSession,
                                      db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                      db_movies : tuple[list[int], list[MovieType]]
                                    ) -> None:
        rating_list = [10, 10, 5]
        movie_id = db_movies[0][0]
        for user_id, rating in zip(db_users[1], rating_list):
            model = RateMovieIn(rating = rating, movie_id = movie_id)
            model._user_id = user_id
            await RatingDAO.rate_movie(model, session = session)
            await session.commit()
            
        for user_id in db_users[1]:
            model = DeleteRateMovieIn(movie_id = movie_id)
            model._user_id = user_id
            await RatingDAO.delete_rate_movie(session, model)
        
        await session.commit()
        
        movie = await session.get(MovieDB, movie_id)
        assert movie.movie_rating_count == 0
        assert movie.movie_rating_sum == 0
        
        
    @staticmethod
    async def test_user_delete_with_incorrect_id(session : AsyncSession,
                                                db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                                db_movies : tuple[list[int], list[MovieType]]
                                                ) -> None:
        user_id = db_users[1][0]
        movie_id = db_movies[0][-1] + 1
        model = DeleteRateMovieIn(movie_id = movie_id)
        model._user_id = user_id
        with pytest.raises(RatingException) as error:
            await RatingDAO.delete_rate_movie(session, model)
            
        assert error.value.detail['ditail']['type'] == RateErrorType.RATE_NOT_FOUND
     
        