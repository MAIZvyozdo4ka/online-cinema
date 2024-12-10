from .schemas import ReviewMovieWithUserInfoOut, ReviewMovieWithUserInfoListWithStatisticOut, ReviewMovie
from core.models.postgres import ReviewDB, StatementReviewType
from core.dao import PostgresDAO, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class MovieRewivewDAO(PostgresDAO):
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_user_review_by_user_id(cls,
                                          session : AsyncSession,
                                          movie_id : int,
                                          user_id : int
                                        ) -> ReviewMovie | None:
    
        user_movie_review = await session.get(ReviewDB, (movie_id, user_id))
        if user_movie_review is not None:
            return ReviewMovie.model_validate(user_movie_review)
    
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_movie_reviews(cls,
                                session : AsyncSession,
                                movie_id : int,
                                limit : int | None = None,
                                offset : int | None = None
                            ) -> list[ReviewMovieWithUserInfoOut]:
        query_for_select_movies_reviews = select(ReviewDB).options(
                                                            selectinload(ReviewDB.user)
                                                        ).where(
                                                            ReviewDB.movie_id == movie_id
                                                        ).order_by(
                                                            ReviewDB.updated_at.desc(), ReviewDB.user_id
                                                        )
        if limit is not None:
            query_for_select_movies_reviews = query_for_select_movies_reviews.limit(limit)
        
        if offset is not None:
            query_for_select_movies_reviews = query_for_select_movies_reviews.offset(offset)
        
        movie_reviews = await session.scalars(query_for_select_movies_reviews)
        return [ReviewMovieWithUserInfoOut.model_validate(review) for review in movie_reviews]
        
    
    @classmethod
    async def get_movie_reviews_with_statistic(cls, movie_id : int) -> ReviewMovieWithUserInfoListWithStatisticOut:
        movies_reveiws : list[ReviewMovieWithUserInfoOut] = await cls.get_movie_reviews(movie_id = movie_id)
        reviews_count = len(movies_reveiws)
        statement_percent : dict[StatementReviewType, int] = {
                                                            StatementReviewType.negative : 0,
                                                            StatementReviewType.neutral : 0,
                                                            StatementReviewType.positive : 0
                                                        }
        for review in movies_reveiws:
            statement_percent[review.statement] += 1
        
        for statement, count in statement_percent.items():
            statement_percent[statement] = round(count * 100 / reviews_count, 2)
        
        return ReviewMovieWithUserInfoListWithStatisticOut(
                                                            reviews = movies_reveiws,
                                                            reviews_count = reviews_count,
                                                            positive_statement_percent = statement_percent[StatementReviewType.positive],
                                                            negative_statement_percent = statement_percent[StatementReviewType.negative],
                                                            neutral_statement_percent = statement_percent[StatementReviewType.neutral]
                                                        )