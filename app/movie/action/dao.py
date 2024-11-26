from .schemas import MovieOut, MovieWithUserInfoOut, MovieRatingOut, ReviewMovieWithUserInfoOut, ReviewMovieWithUserInfoListWithStatisticOut
from app.database import MovieDB, RatingDB, ReviewDB, StatementReviewType
from .errors import MovieNotFoundError
from app.BaseDAO import BaseDAO, AsyncSession
from sqlalchemy import select, func
from app.user.movie_action.dao import UserActionDAO
from sqlalchemy.orm import selectinload


class MovieDAO(BaseDAO):
    
    
    @classmethod
    @BaseDAO.get_session()
    async def get_movie_reviews(cls,
                                session : AsyncSession,
                                movie_id : int,
                                limit : int | None = None
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
        
        movie_reviews = await session.scalars(query_for_select_movies_reviews)
        return [ReviewMovieWithUserInfoOut.model_validate(review) for review in movie_reviews]
        
        
        
    
    @classmethod
    @BaseDAO.get_session()
    async def get_movie_by_id(cls,
                              session : AsyncSession,
                              movie_id : int,
                              user_id : int | None = None
                            ) -> MovieWithUserInfoOut:
        movie = await session.get(MovieDB, movie_id)
        
        if movie is None:
            raise MovieNotFoundError
        
        return MovieWithUserInfoOut(
                                movie = MovieOut.model_validate(movie),
                                user_info = await UserActionDAO.get_all_user_actions_with_movie(session, movie_id, user_id),
                                reviews = await cls.get_movie_reviews(session, movie_id, 5)
                            )
    
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