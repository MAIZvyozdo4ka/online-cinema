from .schemas import (RateMovieIn,
                      DeleteRateMovieIn,
                      RateMovieOut,
                      ShowUserMovieRatingListOut,
                      ShowUserMovieRatingOut
                    )
from core.models.postgres import RatingDB
from .errors import RateNotFoundError, MovieNotFoundError
from core.dao import PostgresDAO, AsyncSession, UserActionDAO
from core.schemas import SuccessUserActionStatusType



class RatingDAO(UserActionDAO):
    

    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def update_user_movie_rating(cls, session : AsyncSession, rating_form : RateMovieIn) -> RateMovieOut:
        await cls.update_user_movie_rating_or_review(session, RatingDB, rating_form)
        return RateMovieOut(status = SuccessUserActionStatusType.SUCCESS_UPDATE)
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def try_insert_user_movie_rating(cls, session : AsyncSession, rating_form : RateMovieIn) -> RateMovieOut:
        await cls.try_insert_user_movie_rating_review(session, RatingDB, rating_form)
        
        return RateMovieOut(status = SuccessUserActionStatusType.SUCCESS_INSERT)

        
    
    
    @classmethod
    async def rate_movie(cls, rating_form : RateMovieIn) -> RateMovieOut:
        return await cls.review_or_rate_movie(
                                            cls.try_insert_user_movie_rating,
                                            cls.update_user_movie_rating,
                                            rating_form,
                                            MovieNotFoundError
                                        )
              
        
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def delete_rate_movie(cls, session : AsyncSession, delete_form : DeleteRateMovieIn) -> RateMovieOut:
        rating = await cls.delete_user_rating_or_review_movie(session, RatingDB, delete_form)
        
        if rating is None:
            raise RateNotFoundError
        
        return RateMovieOut(status = SuccessUserActionStatusType.SUCCESS_DELETE)
    
    
    @classmethod     
    async def get_user_movies_rating(cls, user_id : int) -> ShowUserMovieRatingListOut:
        ratings_with_movies = await cls.get_user_movies_rating_or_reviews(RatingDB, user_id)
        return ShowUserMovieRatingListOut(
                                        rate_list = [ShowUserMovieRatingOut.model_validate(rating) for rating in ratings_with_movies]
                                    )
        