from fastapi import APIRouter, Query, Request
from typing import Annotated
from .schemas import MoviePreviewOut, TextSearchIn
from .dao import SearchDAO
from .errors import SearchHTTPException



router = APIRouter(prefix = '/search', tags = ['Поиск'], responses = SearchHTTPException.get_responses_schemas())



@router.get(path = '', summary = 'Поиск фильмов')
async def search(parametrs : Annotated[TextSearchIn, Query()]) -> list[MoviePreviewOut]:

    return await SearchDAO.search_movies_by_input_text(text = parametrs.text)



    