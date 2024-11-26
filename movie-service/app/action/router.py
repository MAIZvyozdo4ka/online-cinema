from fastapi import APIRouter, Request, Path
from typing import Annotated
from pydantic import PositiveInt
from .schemas import MovieOut
from .dao import MovieDAO
from .errors import MovieHTTPExeption


router = APIRouter(prefix = '/movie/{movie_id}',
                   tags = ['Фильмы'],
                   responses = MovieHTTPExeption.get_responses_schemas()
                )




@router.get(path = '', summary = 'Поиск фильма по ID')
async def get_movie_by_id(request : Request, movie_id : Annotated[PositiveInt, Path(le = 10_000_000)]) -> MovieOut:
    return await MovieDAO.get_movie_by_id(movie_id)

