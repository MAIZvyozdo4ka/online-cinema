from tests.Base import TestBase, MovieType
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from review_service.app.review.dao import ReviewDAO
from review_service.app.review.schemas import ReviewMovieIn, DeleteReviewMovieIn
from core.dependencies.JWTToken import IssuedJWTTokensOut
from core.models.postgres import StatementReviewType
from moderator_service.app.reviews.dao import ModeratorRewivewDAO
from moderator_service.app.reviews.errors import ModeratorReviewException, ModeratorReviewErrorType



class TestModerator(TestBase):
    
    
    
    @staticmethod
    async def test_get_all_reviews(session : AsyncSession,
                                  db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                  db_movies : tuple[list[int], list[MovieType]]
                                ) -> None:
        review_review = ['test_review1', 'test_review2', 'test_review3']
        review_header = ['test_header1', 'test_header2', 'test_header3']
        review_statement = [StatementReviewType.positive, StatementReviewType.negative, StatementReviewType.neutral]
        for user_id in db_users[1]:
            for movie_id, review, header, statement in zip(db_movies[0], review_review, review_header, review_statement):
                model = ReviewMovieIn(review = review, movie_id = movie_id, header = header, statement = statement)
                model._user_id = user_id
                await ReviewDAO.review_movie(model, session = session)
                await session.commit()
        user_reviews = await ModeratorRewivewDAO.get_all_reviews(session, len(db_movies[0]) * len(db_users[1]))
        user_review_counter = 0
        for user_id in db_users[1]:
            for movie_id, review, header, statement in zip(db_movies[0], review_review, review_header, review_statement):
                assert user_reviews[user_review_counter].movie_id == movie_id
                assert user_reviews[user_review_counter].review == review
                assert user_reviews[user_review_counter].statement == statement
                assert user_reviews[user_review_counter].header == header
                assert user_reviews[user_review_counter].user.user_id == user_id
                user_review_counter += 1
        
        
    @staticmethod
    async def test_get_all_reviews_with_single_movie(session : AsyncSession,
                                                      db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                                      db_movies : tuple[list[int], list[MovieType]]
                                                    ) -> None:
        review_review = ['test_review1', 'test_review2', 'test_review3']
        review_header = ['test_header1', 'test_header2', 'test_header3']
        review_statement = [StatementReviewType.positive, StatementReviewType.negative, StatementReviewType.neutral]
        movie_id = db_movies[0][0]
        for user_id, review, header, statement in zip( db_users[1], review_review, review_header, review_statement):
            model = ReviewMovieIn(review = review, movie_id = movie_id, header = header, statement = statement)
            model._user_id = user_id
            await ReviewDAO.review_movie(model, session = session)
            await session.commit()
        user_reviews = await ModeratorRewivewDAO.get_all_reviews(session, len(db_users[1]))
        user_review_counter = 0
        for user_id, review, header, statement in zip(db_users[1], review_review, review_header, review_statement):
            assert user_reviews[user_review_counter].movie_id == movie_id
            assert user_reviews[user_review_counter].review == review
            assert user_reviews[user_review_counter].statement == statement
            assert user_reviews[user_review_counter].header == header
            assert user_reviews[user_review_counter].user.user_id == user_id
            user_review_counter += 1
            
            
    @staticmethod
    async def test_get_all_reviews_with_empty(session : AsyncSession,
                                              db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                              db_movies : tuple[list[int], list[MovieType]]
                                            ) -> None:
        user_reviews = await ModeratorRewivewDAO.get_all_reviews(session, 0)
        assert len(user_reviews) == 0
    
            
    
    @staticmethod
    async def test_delete_reviews(session : AsyncSession,
                                  db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                  db_movies : tuple[list[int], list[MovieType]]
                                ) -> None:
        user_reviews = await ModeratorRewivewDAO.get_all_reviews(session, 0)
        assert len(user_reviews) == 0
        review_review = ['test_review1', 'test_review2', 'test_review3']
        review_header = ['test_header1', 'test_header2', 'test_header3']
        review_statement = [StatementReviewType.positive, StatementReviewType.negative, StatementReviewType.neutral]
        for user_id in db_users[1]:
            for movie_id, review, header, statement in zip(db_movies[0], review_review, review_header, review_statement):
                model = ReviewMovieIn(review = review, movie_id = movie_id, header = header, statement = statement)
                model._user_id = user_id
                await ReviewDAO.review_movie(model, session = session)
                await session.commit()
        
        for user_id in db_users[1]:
            for movie_id in db_movies[0]:
                model = DeleteReviewMovieIn(movie_id = movie_id)
                model._user_id = user_id
                await ModeratorRewivewDAO.delete_review(session, model)
        
        for user_id in db_users[1]:
            user_reviews = await ReviewDAO.get_user_movies_reviews(session, user_id)
            assert user_reviews.reviews_count == 0
        
        
    
    @staticmethod
    async def test_delete_reviews_with_incorrect_id(session : AsyncSession,
                                                  db_users : tuple[list[dict[str, str]], list[int], list[IssuedJWTTokensOut]],
                                                  db_movies : tuple[list[int], list[MovieType]]
                                                ) -> None:
        review_review = ['test_review1', 'test_review2', 'test_review3']
        review_header = ['test_header1', 'test_header2', 'test_header3']
        review_statement = [StatementReviewType.positive, StatementReviewType.negative, StatementReviewType.neutral]
        movie_id = db_movies[0][0]
        for user_id, review, header, statement in zip( db_users[1], review_review, review_header, review_statement):
            model = ReviewMovieIn(review = review, movie_id = movie_id, header = header, statement = statement)
            model._user_id = user_id
            await ReviewDAO.review_movie(model, session = session)
            await session.commit()
        
        for user_id in db_users[1]:
            with pytest.raises(ModeratorReviewException) as error:
                model = DeleteReviewMovieIn(movie_id = movie_id + 1)
                model._user_id = user_id
                await ModeratorRewivewDAO.delete_review(session, model)
            assert error.value.detail['ditail']['type'] == ModeratorReviewErrorType.REVIEW_NOT_FOUND