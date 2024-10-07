from search.schemas import MovieResponse, LinkResponse, TextSearchRequest
from database import Link, Movie, async_session_maker
from sqlalchemy import select
from typing import Any


class SearchDAO:
    
    @classmethod
    async def search_movies_by_input_text(
                                        cls,
                                        text : str | None = None,
                                        movie_count : int = 5
                                    ) -> list[MovieResponse]:
        
        response_list_of_movies : list[dict[str, Any]]
        text_for_transaction : str = text if text is not None else ''
        
        async with async_session_maker() as session:
            query = select(Movie).where(Movie.title.like(f'%{text_for_transaction}%')).limit(movie_count)
            movies = await session.execute(query)
            response_list_of_movies = [MovieResponse.model_validate(movie) for movie in movies.scalars()]
            await session.rollback()
        
        return response_list_of_movies
        