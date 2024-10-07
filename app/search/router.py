from fastapi import APIRouter, Query, Request
from typing import Annotated
from search.schemas import MovieResponse, TextSearchRequest
from search.dao import SearchDAO



router = APIRouter(prefix = '/search', tags = ['Поиск'])


@router.get(path = '/', summary = 'Поиск фильмов')
async def search(parametrs : Annotated[TextSearchRequest, Query()]) -> list[MovieResponse]:

    return await SearchDAO.search_movies_by_input_text(text = parametrs.text)
    