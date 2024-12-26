from core.dao import PostgresDAO, AsyncSession, UserActionDAO
from .schemas import ReviewMovieIn, ReviewMovieOut, DeleteReviewMovieIn, ShowUserMovieReviewsListOut, ShowUserMovieReviewsOut
from .errors import ReviewNotFoundError, MovieNotFoundError
from core.models.postgres import ReviewDB
from core.schemas import SuccessUserActionStatusType



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
    async def review_movie(cls, review : ReviewMovieIn, session : AsyncSession | None = None) -> ReviewMovieOut:
        
        return await UserActionDAO.review_or_rate_movie(
                                                    cls.try_insert_user_movie_review,
                                                    cls.update_user_movie_review,
                                                    review,
                                                    MovieNotFoundError,
                                                    session
                                                )
        
        
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def delete_review_movie(cls, session : AsyncSession, deleted_form : DeleteReviewMovieIn) -> ReviewMovieOut:
        review = await UserActionDAO.delete_user_rating_or_review_movie(session, ReviewDB, deleted_form)
        
        if review is None:
            raise ReviewNotFoundError
        
        return ReviewMovieOut(status = SuccessUserActionStatusType.SUCCESS_DELETE)
    
    
    @classmethod    
    @PostgresDAO.get_session()
    async def get_user_movies_reviews(cls, session : AsyncSession, user_id : int) -> ShowUserMovieReviewsListOut:
        reviews_with_movies = await UserActionDAO.get_user_movies_rating_or_reviews(session, ReviewDB, user_id)
        return ShowUserMovieReviewsListOut(
                                        reviews_list = [ShowUserMovieReviewsOut.model_validate(review) for review in reviews_with_movies]
                                    )
    