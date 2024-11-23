from .schemas import RateMovieIn, DeleteRateMovieIn, RateMovieOut
from app.database import RatingDB
from .errors import RateNotFoundError, MovieNotFoundError
from app.BaseDAO import BaseDAO, AsyncSession
from app.user.movie_action.dao import UserActionDAO
from app.user.movie_action.schemas import SuccessUserActionStatusType



class RatingDAO(BaseDAO):
    

    @classmethod
    @BaseDAO.get_session(auto_commit = True)
    async def update_user_movie_rating(cls, session : AsyncSession, rating_form : RateMovieIn) -> RateMovieOut:
        await UserActionDAO.update_user_movie_rating_or_review(session, RatingDB, rating_form)
        return RateMovieOut(status = SuccessUserActionStatusType.SUCCESS_UPDATE)
    
    
    
    @classmethod
    @BaseDAO.get_session(auto_commit = True)
    async def try_insert_user_movie_rating(cls, session : AsyncSession, rating_form : RateMovieIn) -> RateMovieOut:
        await UserActionDAO.try_insert_user_movie_rating_review(session, RatingDB, rating_form)
        
        return RateMovieOut(status = SuccessUserActionStatusType.SUCCESS_INSERT)

        
    
    
    @classmethod
    async def rate_movie(cls, rating_form : RateMovieIn) -> RateMovieOut:
        return await UserActionDAO.review_or_rate_movie(
                                                    cls.try_insert_user_movie_rating,
                                                    cls.update_user_movie_rating,
                                                    rating_form,
                                                    MovieNotFoundError
                                                )
              
        
    
    @classmethod
    @BaseDAO.get_session(auto_commit = True)
    async def delete_rate_movie(cls, session : AsyncSession, delete_form : DeleteRateMovieIn) -> RateMovieOut:
        rating = await UserActionDAO.delete_user_rating_or_review_movie(session, RatingDB, delete_form)
        
        if rating is None:
            raise RateNotFoundError
        
        return RateMovieOut(status = SuccessUserActionStatusType.SUCCESS_DELETE)
    
    
    
    
    
            
            