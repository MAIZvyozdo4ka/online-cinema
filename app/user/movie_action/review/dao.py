from app.PostgresDAO import PostgresDAO, AsyncSession
from .schemas import ReviewMovieIn, ReviewMovieOut, DeleteReviewMovieIn
from .errors import ReviewNotFoundError, MovieNotFoundError
from app.database import ReviewDB
from app.user.movie_action.dao import UserActionDAO
from app.user.movie_action.schemas import SuccessUserActionStatusType



class ReviewDAO(PostgresDAO):
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def try_insert_user_movie_review(cls, session : AsyncSession, review : ReviewMovieIn) -> ReviewMovieOut:
        await UserActionDAO.try_insert_user_movie_rating_review(session, ReviewDB, review)
        
        return ReviewMovieOut(status = SuccessUserActionStatusType.SUCCESS_INSERT)
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def update_user_movie_review(cls, session : AsyncSession, updated_review : ReviewMovieIn) -> ReviewMovieOut:
        await UserActionDAO.update_user_movie_rating_or_review(session, ReviewDB, updated_review)
        return ReviewMovieOut(status = SuccessUserActionStatusType.SUCCESS_UPDATE)
     
    
    
    @classmethod
    async def review_movie(cls, review : ReviewMovieIn) -> ReviewMovieOut:
        
        return await UserActionDAO.review_or_rate_movie(
                                                    cls.try_insert_user_movie_review,
                                                    cls.update_user_movie_review,
                                                    review,
                                                    MovieNotFoundError
                                                )
        
        
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def delete_review_movie(cls, session : AsyncSession, deleted_form : DeleteReviewMovieIn) -> ReviewMovieOut:
        review = await UserActionDAO.delete_user_rating_or_review_movie(session, ReviewDB, deleted_form)
        
        if review is None:
            raise ReviewNotFoundError
        
        return ReviewMovieOut(status = SuccessUserActionStatusType.SUCCESS_DELETE)
    
    