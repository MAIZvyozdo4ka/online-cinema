from .PostgresDAO import PostgresDAO, AsyncSession
from sqlalchemy import delete, insert, update, ScalarResult, select
from core.schemas import BaseDeletedModel, ModelWithPrivateUserIdAndMovieId, UserActionOut
from core.models.postgres import RatingDB, ReviewDB
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy.exc import IntegrityError
from typing import Callable
from sqlalchemy.orm import selectinload
from core.exception import BaseHTTPException




class UserActionDAO(PostgresDAO):
        
    @classmethod
    async def delete_user_rating_or_review_movie(cls,   
                                                session : AsyncSession,
                                                db_model : type[RatingDB] | type[ReviewDB],
                                                deleted_form : BaseDeletedModel
                                            ) -> int | None:
        query_for_delete = delete(db_model).where(
                                        db_model.movie_id == deleted_form.movie_id,
                                        db_model.user_id == deleted_form.user_id
                                    ).returning(
                                        db_model.movie_id
                                    )
                                    
        return await session.scalar(query_for_delete)
    
    
    @classmethod
    async def try_insert_user_movie_rating_review(cls,
                                                   session : AsyncSession,
                                                   db_model : type[RatingDB] | type[ReviewDB],
                                                   insert_form : ModelWithPrivateUserIdAndMovieId
                                                ) -> None:
        query_for_insert_user_movie_rating_or_review = insert(db_model).values(insert_form.model_dump())
        try:
            await session.execute(query_for_insert_user_movie_rating_or_review)
        except IntegrityError as error:
            if error.orig.__dict__['pgcode'] == '23505':
                raise UniqueViolationError
            if error.orig.__dict__['pgcode'] == '23503':
                raise ForeignKeyViolationError
            
            
    @classmethod
    async def update_user_movie_rating_or_review(cls,
                                                session : AsyncSession,
                                                db_model : type[RatingDB] | type[ReviewDB],
                                                updated_form : ModelWithPrivateUserIdAndMovieId
                                            ) -> None:
        dump_form = updated_form.model_dump(exclude = {'movie_id', 'user_id'})
        query_for_update_user_movie_rating_or_review = update(db_model).where(
                                                                    db_model.user_id == updated_form.user_id,
                                                                    db_model.movie_id == updated_form.movie_id
                                                            ).values(dump_form)
                                                                
        await session.execute(query_for_update_user_movie_rating_or_review)
        
        
    @classmethod
    async def review_or_rate_movie(cls,
                                   inserted_func : Callable[[ModelWithPrivateUserIdAndMovieId], UserActionOut],
                                   updated_func : Callable[[ModelWithPrivateUserIdAndMovieId], UserActionOut],
                                   form : ModelWithPrivateUserIdAndMovieId,
                                   error : BaseHTTPException
                                ) -> UserActionOut:
        try:
            return await inserted_func(form)
        except UniqueViolationError:
            return await updated_func(form)
        except ForeignKeyViolationError:
            raise error
        
        
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
        
    