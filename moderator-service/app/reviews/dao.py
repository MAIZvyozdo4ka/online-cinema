from .schemas import ReviewMovieWithUserInfoAndMovieIDOut
from core.models.postgres import ReviewDB, StatementReviewType
from core.dao import PostgresDAO, AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from .schemas import DeleteReviewIn
from .errors import ReviewNotFoundError



class ModeratorRewivewDAO(PostgresDAO):
    
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_all_reviews(cls,
                                session : AsyncSession,
                                limit : int,
                                offset : int | None = None,
                                statement : StatementReviewType | None = None
                            ) -> list[ReviewMovieWithUserInfoAndMovieIDOut]:
        
        query_for_select_movies_reviews = select(ReviewDB).options(
                                                            selectinload(ReviewDB.user)
                                                        ).order_by(
                                                                ReviewDB.updated_at.desc(), ReviewDB.user_id
                                                            ).limit(
                                                                limit
                                                            )                                       
        if statement is not None:
            query_for_select_movies_reviews = query_for_select_movies_reviews.where(ReviewDB.statement == statement)
        
        if offset is not None:
            query_for_select_movies_reviews = query_for_select_movies_reviews.offset(offset)
        
        movie_reviews = await session.scalars(query_for_select_movies_reviews)
        return [ReviewMovieWithUserInfoAndMovieIDOut.model_validate(review) for review in movie_reviews]
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def delete_review(cls, session : AsyncSession, delete_form : DeleteReviewIn) -> None:
        query_for_delete_review = delete(ReviewDB).where(
                                                            ReviewDB.movie_id == delete_form.movie_id,
                                                            ReviewDB.user_id == delete_form.user_id
                                                        ).returning(ReviewDB.user_id)
        user_id = await session.scalar(query_for_delete_review)
        
        if user_id is None:
            raise ReviewNotFoundError 