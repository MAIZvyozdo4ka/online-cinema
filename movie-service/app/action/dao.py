from .schemas import MovieOut
from core.models.postgres import MovieDB
from .errors import MovieNotFoundError
from core.dao import BaseDAO, AsyncSession


class MovieDAO(BaseDAO):
        
    
    @classmethod
    @BaseDAO.get_session()
    async def get_movie_by_id(cls,
                              session : AsyncSession,
                              movie_id : int
                            ) -> MovieOut:
        movie = await session.get(MovieDB, movie_id)
        
        if movie is None:
            raise MovieNotFoundError
        
        return MovieOut.model_validate(movie)