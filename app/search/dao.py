from .schemas import MoviePreviewOut
from database import MovieDB, async_session_maker
from sqlalchemy import select
from typing import Any
from .errors import SearchEmptyError



class SearchDAO:
    
    @classmethod
    async def search_movies_by_input_text(
                                        cls,
                                        text : str | None = None,
                                        movie_count : int = 5
                                    ) -> list[MoviePreviewOut]:
        
        response_list_of_movies : list[dict[str, Any]]
        text_for_transaction : str = text if text is not None else ''
        
        async with async_session_maker() as session:
            query = select(MovieDB).where(MovieDB.title.like(f'%{text_for_transaction}%')).limit(movie_count)
            movies = await session.scalars(query)
            response_list_of_movies = [MoviePreviewOut.model_validate(movie) for movie in movies]
        
        if not response_list_of_movies:
            raise SearchEmptyError
            
        return response_list_of_movies
    
    
    
    @classmethod
    async def get_movie_by_id(cls, moive_id : int) -> MoviePreviewOut:
        async with async_session_maker() as session:
            
            movie = await session.get(MovieDB, moive_id)
            
            if movie is None:
                raise SearchEmptyError
        
            return MoviePreviewOut.model_validate(movie)
        
            
    

        