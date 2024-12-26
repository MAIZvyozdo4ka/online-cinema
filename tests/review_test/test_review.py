from tests.Base import TestBase, MovieType
from core.models.postgres import MovieDB
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from review_service.app.review.dao import ReviewDAO
from review_service.app.review.errors import ReviewException, ReviewErrorType
from review_service.app.review.schemas import ReviewMovieIn, DeleteReviewMovieIn
from core.dependencies.JWTToken import IssuedJWTTokensOut
from core.models.postgres import ReviewDB, StatementReviewType
from sqlalchemy import select





class TestReview(TestBase):
    
    
    
    @staticmethod
    async def test_users_review(session : AsyncSession,
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
        
        movie_review = await session.scalars(select(ReviewDB).where(ReviewDB.movie_id == movie_id).order_by(ReviewDB.user_id))
        movie_review = movie_review.all()
        assert len(movie_review) == len(db_users[1])
        for db_review, user_id, review, header, statement in zip(movie_review, db_users[1], review_review, review_header, review_statement):
            assert db_review.header == header
            assert db_review.review == review
            assert db_review.statement == statement
            assert db_review.user_id == user_id
        
        
        
    @staticmethod
    async def test_user_single_review(
                            session : AsyncSession,
                              db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                              db_movies : tuple[list[int], list[MovieType]]
                            ) -> None:
    
        review_review = ['test_review1', 'test_review2', 'test_review3']
        review_header = ['test_header1', 'test_header2', 'test_header3']
        review_statement = [StatementReviewType.positive, StatementReviewType.negative, StatementReviewType.neutral]
        movie_id = db_movies[0][0]
        user_id = db_users[1][0]
        for review, header, statement in zip(review_review, review_header, review_statement):
            model = ReviewMovieIn(review = review, movie_id = movie_id, header = header, statement = statement)
            model._user_id = user_id
            await ReviewDAO.review_movie(model, session = session)
            await session.commit()
        
        movie_review = await session.scalars(select(ReviewDB).where(ReviewDB.movie_id == movie_id).order_by(ReviewDB.user_id))
        movie_review = movie_review.all()
        assert len(movie_review) == 1
        assert movie_review[0].header == review_header[-1]
        assert movie_review[0].review == review_review[-1]
        assert movie_review[0].statement == review_statement[-1]
        
        
    @staticmethod
    async def test_users_review_with_incorrect_movie_id(session : AsyncSession,
                                                      db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                                      db_movies : tuple[list[int], list[MovieType]]
                                                    ) -> None:
        movie_id = db_movies[0][-1] + 1
        with pytest.raises(ReviewException) as error:
            model = ReviewMovieIn(review = 'test_review', header = 'test_header', statement = StatementReviewType.negative, movie_id = movie_id)
            model._user_id = db_users[1][0]
            await ReviewDAO.review_movie(model, session = session)
            await session.commit()
            
        assert error.value.detail['ditail']['type'] == ReviewErrorType.MOVIE_NOT_FOUND
     
        
        
    @staticmethod
    async def test_user_view_review(session : AsyncSession,
                                  db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                  db_movies : tuple[list[int], list[MovieType]]
                                ) -> None:
        review_review = ['test_review1', 'test_review2', 'test_review3']
        review_header = ['test_header1', 'test_header2', 'test_header3']
        review_statement = [StatementReviewType.positive, StatementReviewType.negative, StatementReviewType.neutral]
        user_id = db_users[1][0]
        for movie_id, review, header, statement in zip(db_movies[0], review_review, review_header, review_statement):
            model = ReviewMovieIn(review = review, movie_id = movie_id, header = header, statement = statement)
            model._user_id = user_id
            await ReviewDAO.review_movie(model, session = session)
            await session.commit()
        user_review = await ReviewDAO.get_user_movies_reviews(session, user_id)
        assert user_review.reviews_count == len(db_movies[1])
        for db_review, review, header, statement, movie in zip(user_review.reviews_list, review_review, review_header, review_statement, db_movies[1]):
            assert db_review.header == header
            assert db_review.review == review
            assert db_review.statement == statement
            assert db_review.movie.title == movie['title']
            
    
    @staticmethod
    async def test_user_view_empty_review(session : AsyncSession,
                                        db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                        db_movies : tuple[list[int], list[MovieType]]
                                        ) -> None:
        user_id = db_users[1][0]
        user_review = await ReviewDAO.get_user_movies_reviews(session, user_id)
        assert user_review.reviews_count == 0
        assert user_review.reviews_list == []
        
        
        
    @staticmethod
    async def test_users_review_delete(session : AsyncSession,
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
            
        for user_id in db_users[1]:
            model = DeleteReviewMovieIn(movie_id = movie_id)
            model._user_id = user_id
            await ReviewDAO.delete_review_movie(session, model)
        
        await session.commit()
        
        reviews = await session.scalars(select(ReviewDB).where(ReviewDB.movie_id == movie_id))
        reviews = reviews.all()
        assert len(reviews) == 0
        
        
    @staticmethod
    async def test_user_delete_with_incorrect_id(session : AsyncSession,
                                                db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                                db_movies : tuple[list[int], list[MovieType]]
                                                ) -> None:
        user_id = db_users[1][0]
        movie_id = db_movies[0][-1] + 1
        model = DeleteReviewMovieIn(movie_id = movie_id)
        model._user_id = user_id
        with pytest.raises(ReviewException) as error:
            await ReviewDAO.delete_review_movie(session, model)
            
        assert error.value.detail['ditail']['type'] == ReviewErrorType.REVIEW_NOT_FOUND
     
        