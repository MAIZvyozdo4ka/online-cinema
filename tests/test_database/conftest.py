import pytest 
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import UserDB, IssuedJWTTokenDB, RatingDB
from sqlalchemy import select, insert
from tests.Base import fixture
from typing import Any
import random
    
    
@fixture(scope = 'function')
async def rate(add_users : list[int], add_movies : list[int]) -> list[dict]:
    return [
        {
            'rating' : random.randint(1, 10),
            'movie_id' : movie_id,
            'user_id' : user_id
        } for user_id in add_users for movie_id in add_movies
    ]
    
    

@fixture(scope = 'function')
async def updated_rate(rate : list[dict]) -> list[dict]:
    new_rate = []
    for rateng in rate:
        new_rating = rateng.copy()
        new_rating['rating'] = random.randint(1, 10)
        new_rate.append(new_rating)
    return new_rate
        
    
@fixture(scope = 'function')
async def add_rate(session : AsyncSession, rate : list[dict]) -> None:
    async with session.begin():
        await session.execute(insert(RatingDB).values(rate))
        
        
        
def _statistic(rate : list[dict], add_movies : list[int]) -> tuple[list[int], list[int]]:
    test_rating_movies = [
                            [   
                                user_rating for user_rating in rate 
                                if user_rating['movie_id'] == movie_id
                            ]
                              for movie_id in add_movies
                        ]
    test_rating_movies_count = [len(i) for i in test_rating_movies]
    test_rating_movies_sum = [sum(j['rating'] for j in i) for i in test_rating_movies]
    return test_rating_movies_sum, test_rating_movies_count
    
    
@fixture(scope = 'function')
async def movie_rate_statistic(rate : list[dict], add_movies : list[int]) -> tuple[list[int], list[int]]:
    return _statistic(rate, add_movies)


@fixture(scope = 'function')
async def movie_updated_rate_statistic(updated_rate : list[dict], add_movies : list[int]) -> tuple[list[int], list[int]]:
    return _statistic(updated_rate, add_movies)