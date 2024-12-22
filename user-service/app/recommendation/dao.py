from .schemas import MoviePreviewOut
from core.models.postgres import MovieDB
from core.models.postgres.Recommendation import RecommedationDB
from sqlalchemy import select
from typing import Any
from .errors import RecEmptyError
from core.dao import PostgresDAO, AsyncSession



class RecDAO(PostgresDAO):
    
    @classmethod
    @PostgresDAO.get_session()
    async def recommendation_by_user_id(
                                        cls,
                                        session : AsyncSession,
                                        user_id: int,
                                        movie_count : int = 20
                                    ) -> list[MoviePreviewOut]:

        response_list_of_movies : list[dict[str, Any]]
        query = select(RecommedationDB.recommedation).where(RecommedationDB.userId == int(user_id))
        rec_movies = list(await session.scalars(query))
        query = select(MovieDB).where(MovieDB.id.in_(*rec_movies)).limit(movie_count)
        movies = await session.scalars(query)
        response_list_of_movies = [MoviePreviewOut.model_validate(movie) for movie in movies]

        if not response_list_of_movies:
            raise RecEmptyError
            
        return response_list_of_movies
    
    
    
            
    

        