import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert, update, delete
from app.database import UserDB, RatingDB, MovieDB
import logging
from tests.Base import TestBase, fixture

    



class TestRatingTriggersInsert(TestBase):
    @staticmethod
    async def test_insert_rating_trigger_execute(session : AsyncSession,
                                                rate : list[dict], 
                                                add_movies : list[int], 
                                                movie_rate_statistic : tuple[list[int], list[int]]
                                            ):
        logging.debug(f'rate : {rate}')
        logging.debug(f'movie_rate_statistic : {movie_rate_statistic}')
        
        async with session.begin():
           await session.execute(insert(RatingDB), rate)
        
        movies = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
        movies = movies.all()
        
        logging.debug(f'movies : {movies}')
        
        for count, movie in enumerate(movies):
            assert movie.movie_rating_sum == movie_rate_statistic[0][count]
            assert movie.movie_rating_count == movie_rate_statistic[1][count]
        
        
    @staticmethod
    async def test_insert_rating_trigger_add(session : AsyncSession,
                                             rate : list[dict],
                                             add_movies : list[int],
                                             movie_rate_statistic : tuple[list[int], list[int]]
                                            ):
        logging.debug(f'rate : {rate}')
        logging.debug(f'movie_rate_statistic : {movie_rate_statistic}')
        
        async with session.begin():
            session.add_all([RatingDB(**rating) for rating in rate])
        
        movies = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
        movies = movies.all()
        
        logging.debug(f'movies : {movies}')
        
        for count, movie in enumerate(movies):
            assert movie.movie_rating_sum == movie_rate_statistic[0][count]
            assert movie.movie_rating_count == movie_rate_statistic[1][count]
            
    @staticmethod
    async def test_insert_rating_trigger_value(session : AsyncSession,
                                               rate : list[dict],
                                               add_movies : list[int],
                                               movie_rate_statistic : tuple[list[int], list[int]]
                                            ):
        logging.debug(f'rate : {rate}')
        logging.debug(f'movie_rate_statistic : {movie_rate_statistic}')
        
        async with session.begin():
           await session.execute(insert(RatingDB).values(rate))
        
        movies = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
        movies = movies.all()
        
        logging.debug(f'movies : {movies}')
        
        for count, movie in enumerate(movies):
            assert movie.movie_rating_sum == movie_rate_statistic[0][count]
            assert movie.movie_rating_count == movie_rate_statistic[1][count]
            
    
    @staticmethod
    async def test_insert_rating_trigger_error_empty_user(session : AsyncSession,
                                                           add_rate : None,
                                                           add_users : list[int],
                                                           add_movies : list[int],
                                                           movie_rate_statistic : tuple[list[int], list[int]]
                                                        ):
        empty_user_id = add_users[-1] + 1
        with pytest.raises(IntegrityError):
            async with session.begin():
                await session.execute(insert(RatingDB), [
                                                            {
                                                                'rating' : 10,
                                                                'movie_id' : movie_id,
                                                                'user_id' : empty_user_id
                                                            }
                                                            for movie_id in add_movies
                                                        ]
                                                    )
        
        movies = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
        movies = movies.all()
        
        logging.debug(f'movies : {movies}')
        
        for count, movie in enumerate(movies):
            assert movie.movie_rating_sum == movie_rate_statistic[0][count]
            assert movie.movie_rating_count == movie_rate_statistic[1][count]
    
    


class TestRatingTriggersUpdate(TestBase):
    
    @staticmethod
    async def test_update_rating_trigger_merge(session : AsyncSession,
                                                add_movies : list[int],
                                                add_rate : None,
                                                updated_rate : list[dict],
                                                movie_updated_rate_statistic : tuple[list[int], list[int]]
                                            ):
        async with session.begin():
            for rating in updated_rate:
                await session.merge(RatingDB(**rating))
                
        movies = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
        movies = movies.all()
        
        logging.debug(f'movies : {movies}')
        
        for count, movie in enumerate(movies):
            assert movie.movie_rating_sum == movie_updated_rate_statistic[0][count]
            assert movie.movie_rating_count == movie_updated_rate_statistic[1][count]
            
    @staticmethod
    async def test_update_rating_trigger_execute(session : AsyncSession,
                                                add_movies : list[int],
                                                add_rate : None,
                                                updated_rate : list[dict],
                                                movie_updated_rate_statistic : tuple[list[int], list[int]]
                                            ):
        
        async with session.begin():
            for rating in updated_rate:
                await session.execute(update(RatingDB).where(
                                        RatingDB.movie_id == rating['movie_id'],
                                        RatingDB.user_id == rating['user_id']
                                    ).values(rating = rating['rating'])
                                )
                
        movies = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
        movies = movies.all()
        
        logging.debug(f'movies : {movies}')
        
        for count, movie in enumerate(movies):
            assert movie.movie_rating_sum == movie_updated_rate_statistic[0][count]
            assert movie.movie_rating_count == movie_updated_rate_statistic[1][count]
        
    @staticmethod
    async def test_update_rating_trigger_error(session : AsyncSession,
                                                add_movies : list[int],
                                                add_users : list[int],
                                                add_rate : None,
                                                movie_rate_statistic : tuple[list[int], list[int]]
                                            ):
        empty_user_id = add_users[-1] + 1
        async with session.begin():
            for movie_id in add_movies:
                await session.execute(update(RatingDB).where(
                                        RatingDB.movie_id == movie_id,
                                        RatingDB.user_id == empty_user_id
                                    ).values(rating = 10)
                                )
                
        movies = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
        movies = movies.all()
        
        logging.debug(f'movies : {movies}')
        
        for count, movie in enumerate(movies):
            assert movie.movie_rating_sum == movie_rate_statistic[0][count]
            assert movie.movie_rating_count == movie_rate_statistic[1][count]
        
        
           

class TestRatingTriggersDelete(TestBase):
    
    @staticmethod
    async def test_update_rating_trigger_delete(session : AsyncSession,
                                                add_movies : list[int],
                                                add_rate : None,
                                                rate : list[dict]
                                            ):
        async with session.begin():
            for rating in rate:
                await session.delete(await session.scalar(select(RatingDB).where(
                                                            RatingDB.movie_id == rating['movie_id'],
                                                            RatingDB.user_id == rating['user_id']
                                                            )
                                                        ))
                
        movies = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
        movies = movies.all()
        
        logging.debug(f'movies : {movies}')
        
        for count, movie in enumerate(movies):
            assert movie.movie_rating_sum == 0
            assert movie.movie_rating_count == 0
            
    
    @staticmethod
    async def test_update_rating_trigger_execute(session : AsyncSession,
                                                add_movies : list[int],
                                                add_rate : None,
                                                rate : list[dict]
                                            ):
        async with session.begin():
            for rating in rate:
                await session.execute(delete(RatingDB).where(
                                                            RatingDB.movie_id == rating['movie_id'],
                                                            RatingDB.user_id == rating['user_id']
                                                        )
                                                    )
                
        movies = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
        movies = movies.all()
        
        logging.debug(f'movies : {movies}')
        
        for count, movie in enumerate(movies):
            assert movie.movie_rating_sum == 0
            assert movie.movie_rating_count == 0
            
            
            
    @staticmethod
    async def test_update_rating_trigger_execute_user_id(session : AsyncSession,
                                                        add_movies : list[int],
                                                        add_users : list[int],
                                                        add_rate : None,
                                                        rate : list[dict]
                                                    ):
        async with session.begin():
            for user_id in add_users:
                await session.execute(delete(RatingDB).where(
                                                            RatingDB.user_id == user_id
                                                        )
                                                    )
                
        movies = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
        movies = movies.all()
        
        logging.debug(f'movies : {movies}')
        
        for count, movie in enumerate(movies):
            assert movie.movie_rating_sum == 0
            assert movie.movie_rating_count == 0
            
    
    @staticmethod
    async def test_update_rating_trigger_error(session : AsyncSession,
                                                add_movies : list[int],
                                                add_users : list[int],
                                                add_rate : None,
                                                rate : list[dict],
                                                movie_rate_statistic : tuple[list[int], list[int]]
                                            ):
        empty_user_id = add_users[-1] + 1
        async with session.begin():
            await session.execute(delete(RatingDB).where(
                                                            RatingDB.user_id == empty_user_id
                                                        )
                                                    )
                
        movies = await session.scalars(select(MovieDB).where(MovieDB.id.in_(add_movies)))
        movies = movies.all()
        
        logging.debug(f'movies : {movies}')
        
        for count, movie in enumerate(movies):
            assert movie.movie_rating_sum == movie_rate_statistic[0][count]
            assert movie.movie_rating_count == movie_rate_statistic[1][count]
            
           
            
        