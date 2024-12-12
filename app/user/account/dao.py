from app.database import RatingDB, ReviewDB, UserDB
from app.JWTToken import JWTTokenDAO
from app.PostgresDAO import PostgresDAO, AsyncSession
from sqlalchemy import select, ScalarResult
from sqlalchemy.orm import selectinload
from .schemas import ShowUserMovieRatingOut, ShowUserMovieRatingListOut, ShowUserMovieReviewsListOut, ShowUserMovieReviewsOut
from app.user.schemas import PrivateUserInfoOut


class UserAccountDAO(PostgresDAO):
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_user_by_user_id(cls, session : AsyncSession, user_id : int) -> PrivateUserInfoOut:
        user = await session.get(UserDB, user_id)
        
        return PrivateUserInfoOut.model_validate(user)
        
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def logout(cls, session : AsyncSession, device_id : str) -> None:
            
        await JWTTokenDAO.delete_user_tokens_by_device_id(session, device_id)
      
      
    @classmethod    
    @PostgresDAO.get_session(auto_commit = True)        
    async def full_logout(cls, session : AsyncSession, user_id : int) -> None:
            
        await JWTTokenDAO.delete_all_user_tokens_by_user_id(session, user_id)
            
    
    @classmethod    
    async def get_user_movies_rating(cls, user_id : int) -> ShowUserMovieRatingListOut:
        ratings_with_movies = await cls.get_user_movies_rating_or_reviews(RatingDB, user_id)
        return ShowUserMovieRatingListOut(
                                        rate_list = [ShowUserMovieRatingOut.model_validate(rating) for rating in ratings_with_movies]
                                    )
        
    @classmethod    
    async def get_user_movies_reviews(cls, user_id : int) -> ShowUserMovieReviewsListOut:
        reviews_with_movies = await cls.get_user_movies_rating_or_reviews(ReviewDB, user_id)
        return ShowUserMovieReviewsListOut(
                                        reviews_list = [ShowUserMovieReviewsOut.model_validate(review) for review in reviews_with_movies]
                                    )
        
        
    @classmethod    
    @PostgresDAO.get_session()
    async def get_user_movies_rating_or_reviews(cls,
                                                session : AsyncSession,
                                                db_model : type[RatingDB] | type[ReviewDB],
                                                user_id : int
                                            ) -> ScalarResult:
        query_for_select_user_movie_rating = select(db_model).options(
                                                                    selectinload(db_model.movie)
                                                                ).where(
                                                                    db_model.user_id == user_id
                                                                ).order_by(
                                                                    db_model.updated_at.desc(), db_model.movie_id
                                                                )
        
        return await session.scalars(query_for_select_user_movie_rating)
        
        
                
            
            
            