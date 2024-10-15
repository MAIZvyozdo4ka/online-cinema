from fastapi import APIRouter, Query, Request, Path
from typing import Annotated
from .schemas import MoviePreviewOut, TextSearchIn
from .dao import SearchDAO
from .errors import SearchHTTPExeption



router = APIRouter(prefix = '/search', tags = ['Поиск'], responses = SearchHTTPExeption.get_responses_schemas())



@router.get(path = '', summary = 'Поиск фильмов')
async def search(parametrs : Annotated[TextSearchIn, Query()]) -> list[MoviePreviewOut]:

    return await SearchDAO.search_movies_by_input_text(text = parametrs.text)



@router.get(path = '/{movie_id}', summary = 'Поиск фильма по ID')
async def search(movie_id : Annotated[int, Path(lt = 2 ** 32)]) -> MoviePreviewOut:

    return await SearchDAO.get_movie_by_id(movie_id)
    