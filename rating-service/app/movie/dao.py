from .schemas import (
                      MovieRatingOut,
                      RateMovie
                    )
from core.models.postgres import RatingDB
from core.dao.BaseDAO import BaseDAO, AsyncSession
from sqlalchemy import select, func


class MovieRatingDAO(BaseDAO):

    @classmethod
    @BaseDAO.get_session()
    async def get_movie_rating_by_id(cls, session : AsyncSession, movie_id : int) -> list[MovieRatingOut]:
        
        query_for_select_rating_grouped_by_rating = select(
                                                            RatingDB.rating,
                                                            func.count(RatingDB.rating)
                                                        ).where(
                                                            RatingDB.movie_id == movie_id
                                                        ).group_by(
                                                            RatingDB.rating
                                                        ).order_by(
                                                            RatingDB.rating
                                                        )
                                                            
        rating_statistic = await session.execute(query_for_select_rating_grouped_by_rating)
        
        return [MovieRatingOut(rating = rating, rating_count = count) for rating, count in rating_statistic.all()]
    
    
    @classmethod
    @BaseDAO.get_session()
    async def get_user_movie_rating_by_user_id(cls,
                                               session : AsyncSession,
                                               movie_id : int,
                                               user_id : int
                                            ) -> RateMovie | None:
        user_movie_rate = await session.get(RatingDB, (movie_id, user_id))
        if user_movie_rate is not None:
            return RateMovie.model_validate(user_movie_rate)