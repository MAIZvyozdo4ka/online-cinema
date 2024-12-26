from tests.Base import TestBase, MovieType
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from rating_service.app.rate.dao import RatingDAO
from rating_service.app.rate.schemas import RateMovieIn
from core.dependencies.JWTToken import IssuedJWTTokensOut
from rating_service.app.movie.dao import MovieRatingDAO
from tests.Base import fixture





class TestMovieRate(TestBase):
    
    
    
    @staticmethod
    async def test_rate_movie(session : AsyncSession,
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
        
        movie_rating = await MovieRatingDAO.get_movie_rating_by_id(session, movie_id)
        assert len(movie_rating) == 2
        assert movie_rating[0].rating == 5
        assert movie_rating[0].rating_count == 1
        assert movie_rating[1].rating == 10
        assert movie_rating[1].rating_count == 2
        
        
    @staticmethod
    async def test_rate_movie_with_same_rate(session : AsyncSession,
                                              db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                              db_movies : tuple[list[int], list[MovieType]]
                                            ) -> None:

        rating_list = [6, 6, 6]
        movie_id = db_movies[0][0]
        for user_id, rating in zip(db_users[1], rating_list):
            model = RateMovieIn(rating = rating, movie_id = movie_id)
            model._user_id = user_id
            await RatingDAO.rate_movie(model, session = session)
            await session.commit()
        
        movie_rating = await MovieRatingDAO.get_movie_rating_by_id(session, movie_id)
        assert len(movie_rating) == 1
        assert movie_rating[0].rating == 6
        assert movie_rating[0].rating_count == 3
        
        
        
    @staticmethod
    async def test_rate_movie_with_deferent_rate(session : AsyncSession,
                                                  db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                                  db_movies : tuple[list[int], list[MovieType]]
                                                ) -> None:

        rating_list = [1, 2, 3]
        movie_id = db_movies[0][0]
        for user_id, rating in zip(db_users[1], rating_list):
            model = RateMovieIn(rating = rating, movie_id = movie_id)
            model._user_id = user_id
            await RatingDAO.rate_movie(model, session = session)
            await session.commit()
        
        movie_rating = await MovieRatingDAO.get_movie_rating_by_id(session, movie_id)
        assert len(movie_rating) == 3
        assert movie_rating[0].rating == 1
        assert movie_rating[0].rating_count == 1
        assert movie_rating[1].rating == 2
        assert movie_rating[1].rating_count == 1
        assert movie_rating[2].rating == 3
        assert movie_rating[2].rating_count == 1
        
        
    @staticmethod
    async def test_empty_rate_movie(session : AsyncSession,
                                      db_movies : tuple[list[int], list[MovieType]]
                                    ) -> None:
        movie_id = db_movies[0][0]
        
        movie_rating = await MovieRatingDAO.get_movie_rating_by_id(session, movie_id)
        assert len(movie_rating) == 0
        
     
    @staticmethod
    async def test_my_rate(session : AsyncSession,
                          db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                          db_movies : tuple[list[int], list[MovieType]]
                        ) -> None:   
        rating_list = [1, 2, 3]
        for user_id, movie_id, rating in zip(db_users[1], db_movies[0], rating_list):
            model = RateMovieIn(rating = rating, movie_id = movie_id)
            model._user_id = user_id
            await RatingDAO.rate_movie(model, session = session)
            await session.commit()
            
        for user_id, movie_id, rating in zip(db_users[1], db_movies[0], rating_list):
            db_rating = await MovieRatingDAO.get_user_movie_rating_by_user_id(session, movie_id, user_id)
            assert db_rating.rating == rating
            
            
    @staticmethod
    async def test_my_rate_with_single_movie(session : AsyncSession,
                                              db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                              db_movies : tuple[list[int], list[MovieType]]
                                            ) -> None:   
        rating_list = [1, 2, 3]
        movie_id = db_movies[0][1]
        for user_id, rating in zip(db_users[1], rating_list):
            model = RateMovieIn(rating = rating, movie_id = movie_id)
            model._user_id = user_id
            await RatingDAO.rate_movie(model, session = session)
            await session.commit()
            
        for user_id, rating in zip(db_users[1], rating_list):
            db_rating = await MovieRatingDAO.get_user_movie_rating_by_user_id(session, movie_id, user_id)
            assert db_rating.rating == rating
            
            
            
    @staticmethod
    async def test_my_empty_rate(session : AsyncSession,
                                  db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                  db_movies : tuple[list[int], list[MovieType]]
                                ) -> None:   
        rating_list = [1, 2, 3]
        for user_id, movie_id, rating in zip(db_users[1], db_movies[0], rating_list):
            model = RateMovieIn(rating = rating, movie_id = movie_id)
            model._user_id = user_id
            await RatingDAO.rate_movie(model, session = session)
            await session.commit()
            
        for user_id, movie_id, rating in zip(db_users[1], db_movies[0], rating_list):
            db_rating = await MovieRatingDAO.get_user_movie_rating_by_user_id(session, movie_id + 1, user_id)
            assert db_rating is None
            