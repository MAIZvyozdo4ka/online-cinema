from .schemas import MoviePreviewOut
from core.models.postgres import MovieDB
from sqlalchemy import select
from typing import Any
from .errors import SearchEmptyError
from core.dao import BaseDAO, AsyncSession



class SearchDAO(BaseDAO):
    
    @classmethod
    @BaseDAO.get_session()
    async def search_movies_by_input_text(
                                        cls,
                                        session : AsyncSession,
                                        text : str | None = None,
                                        movie_count : int = 5
                                    ) -> list[MoviePreviewOut]:
        
        response_list_of_movies : list[dict[str, Any]]
        text_for_transaction : str = text if text is not None else ''
        query = select(MovieDB).where(MovieDB.title.like(f'%{text_for_transaction}%')).limit(movie_count)
        movies = await session.scalars(query)
        response_list_of_movies = [MoviePreviewOut.model_validate(movie) for movie in movies]
        
        if not response_list_of_movies:
            raise SearchEmptyError
            
        return response_list_of_movies
    
    
    
            
    

        