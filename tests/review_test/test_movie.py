from tests.Base import TestBase, MovieType
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from review_service.app.review.dao import ReviewDAO
from review_service.app.review.errors import ReviewException, ReviewErrorType
from review_service.app.review.schemas import ReviewMovieIn, DeleteReviewMovieIn
from core.dependencies.JWTToken import IssuedJWTTokensOut
from core.models.postgres import StatementReviewType
from review_service.app.movie.dao import MovieRewivewDAO




class TestMovieReview(TestBase):
    
    
    
    @staticmethod
    async def test_review_movie(session : AsyncSession,
                              db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                              db_movies : tuple[list[int], list[MovieType]]
                            ) -> None:

        review_review = ['test_review1', 'test_review2', 'test_review3']
        review_header = ['test_header1', 'test_header2', 'test_header3']
        review_statement = [StatementReviewType.positive, StatementReviewType.negative, StatementReviewType.neutral]
        movie_id = db_movies[0][0]
        for user_id, review, header, statement in zip(db_users[1], review_review, review_header, review_statement):
            model = ReviewMovieIn(review = review, movie_id = movie_id, header = header, statement = statement)
            model._user_id = user_id
            await ReviewDAO.review_movie(model, session = session)
            await session.commit()
        
        movie_review = await MovieRewivewDAO.get_movie_reviews_with_statistic(session, movie_id)
        assert movie_review.reviews_count == len(db_users[1])
        assert movie_review.neutral_statement_percent == 33.33
        assert movie_review.negative_statement_percent == 33.33
        assert movie_review.positive_statement_percent == 33.33
        for db_review, review, header, statement in zip(movie_review.reviews, review_review, review_header, review_statement):
            assert db_review.header == header
            assert db_review.statement == statement
            assert db_review.review == review
        
        
    @staticmethod
    async def test_review_movie_with_same_review(session : AsyncSession,
                                              db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                              db_movies : tuple[list[int], list[MovieType]]
                                            ) -> None:

        review = 'test_review'
        header = 'test_header'
        statement = StatementReviewType.positive
        movie_id = db_movies[0][0]
        for user_id in db_users[1]:
            model = ReviewMovieIn(review = review, movie_id = movie_id, header = header, statement = statement)
            model._user_id = user_id
            await ReviewDAO.review_movie(model, session = session)
            await session.commit()
        
        movie_review = await MovieRewivewDAO.get_movie_reviews_with_statistic(session, movie_id)
        assert movie_review.reviews_count == len(db_users[1])
        assert movie_review.neutral_statement_percent == 0
        assert movie_review.negative_statement_percent == 0
        assert movie_review.positive_statement_percent == 100
        for db_review in movie_review.reviews:
            assert db_review.header == header
            assert db_review.statement == statement
            assert db_review.review == review
        
        
        
        
    @staticmethod
    async def test_empty_review_movie(session : AsyncSession,
                                      db_movies : tuple[list[int], list[MovieType]]
                                    ) -> None:
        movie_id = db_movies[0][0]
        
        movie_review = await MovieRewivewDAO.get_movie_reviews_with_statistic(session, movie_id)
        assert len(movie_review.reviews) == 0
        assert movie_review.neutral_statement_percent == 0
        assert movie_review.negative_statement_percent == 0
        assert movie_review.positive_statement_percent == 0
        
     
    @staticmethod
    async def test_my_review(session : AsyncSession,
                              db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                              db_movies : tuple[list[int], list[MovieType]]
                            ) -> None:   
        review_review = ['test_review1', 'test_review2', 'test_review3']
        review_header = ['test_header1', 'test_header2', 'test_header3']
        review_statement = [StatementReviewType.positive, StatementReviewType.negative, StatementReviewType.neutral]
        for user_id, movie_id, review, header, statement in zip(db_users[1], db_movies[0], review_review, review_header, review_statement):
            model = ReviewMovieIn(review = review, movie_id = movie_id, header = header, statement = statement)
            model._user_id = user_id
            await ReviewDAO.review_movie(model, session = session)
            await session.commit()
            
        for user_id, movie_id, review, header, statement in zip(db_users[1], db_movies[0], review_review, review_header, review_statement):
            db_review = await MovieRewivewDAO.get_user_review_by_user_id(session, movie_id, user_id)
            assert db_review.review == review
            assert db_review.statement == statement
            assert db_review.header == header
            
            
    @staticmethod
    async def test_my_review_with_single_movie(session : AsyncSession,
                                              db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                              db_movies : tuple[list[int], list[MovieType]]
                                            ) -> None:   
        review_review = ['test_review1', 'test_review2', 'test_review3']
        review_header = ['test_header1', 'test_header2', 'test_header3']
        review_statement = [StatementReviewType.positive, StatementReviewType.negative, StatementReviewType.neutral]
        movie_id = db_movies[0][0]
        for user_id, review, header, statement in zip(db_users[1], review_review, review_header, review_statement):
            model = ReviewMovieIn(review = review, movie_id = movie_id, header = header, statement = statement)
            model._user_id = user_id
            await ReviewDAO.review_movie(model, session = session)
            await session.commit()
            
        for user_id, review, header, statement in zip(db_users[1], review_review, review_header, review_statement):
            db_review = await MovieRewivewDAO.get_user_review_by_user_id(session, movie_id, user_id)
            assert db_review.review == review
            assert db_review.statement == statement
            assert db_review.header == header
            
            
    @staticmethod
    async def test_my_empty_review(session : AsyncSession,
                                  db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                  db_movies : tuple[list[int], list[MovieType]]
                                ) -> None:   
        review_review = ['test_review1', 'test_review2', 'test_review3']
        review_header = ['test_header1', 'test_header2', 'test_header3']
        review_statement = [StatementReviewType.positive, StatementReviewType.negative, StatementReviewType.neutral]
        for user_id, movie_id, review, header, statement in zip(db_users[1], db_movies[0], review_review, review_header, review_statement):
            model = ReviewMovieIn(review = review, movie_id = movie_id, header = header, statement = statement)
            model._user_id = user_id
            await ReviewDAO.review_movie(model, session = session)
            await session.commit()
            
        for user_id, movie_id, review, header, statement in zip(db_users[1], db_movies[0], review_review, review_header, review_statement):
            db_review = await MovieRewivewDAO.get_user_review_by_user_id(session, movie_id + 1, user_id)
            assert db_review is None
            