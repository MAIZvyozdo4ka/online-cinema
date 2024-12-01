from .schemas import MoviePreviewOut
from core.models.postgres import MovieDB
from sqlalchemy import select
from typing import Any
from .errors import SearchEmptyError
from core.dao import PostgresDAO, AsyncSession
from core.dao.Search import Search



class SearchDAO(PostgresDAO):

    client = Search()

    @classmethod
    @PostgresDAO.get_session()
    async def search_movies_by_input_text(
                                        cls,
                                        session : AsyncSession,
                                        text : str | None = None,
                                        movie_count : int = 5
                                    ) -> list[MoviePreviewOut]:
        
        response_list_of_movies : list[dict[str, Any]]
        movie_ids = await cls.client.search(text)
        query = select(MovieDB).where(MovieDB.id.in_(movie_ids)).limit(movie_count)
        movies = await session.scalars(query)
        response_list_of_movies = [MoviePreviewOut.model_validate(movie) for movie in movies]

        if not response_list_of_movies:
            raise SearchEmptyError
            
        return response_list_of_movies

    async def close_elasticsearch(self):
        await self.client.close()
    
    
            
    

        