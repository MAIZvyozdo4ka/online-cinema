from fastapi import APIRouter, Request, Depends, Path
from core.dependencies.JWTToken import TokenValidation
from pydantic import PositiveInt
from typing import Annotated
from .schemas import MovieRatingOut, RateMovie
from .dao import MovieRatingDAO


router = APIRouter(prefix = '/movie/{movie_id}', tags = ['Оценка фильма'])



@router.get(path = '', summary = 'Статистика оценок фильма')
async def get_movie_retings_by_id(movie_id : Annotated[PositiveInt, Path(le = 10_000_000)]) -> list[MovieRatingOut]:
    return await MovieRatingDAO.get_movie_rating_by_id(movie_id)



@router.get(path = '/my',
            summary = 'Оценка пользователя определенного фильма',
            dependencies = [Depends(TokenValidation.weak_check_access_token)]
        )
async def get_movie_by_id(request : Request, movie_id : Annotated[PositiveInt, Path(le = 10_000_000)]) -> RateMovie | None:
    if request.state.user is None:
        return None
    
    return await MovieRatingDAO.get_user_movie_rating_by_user_id(movie_id,  request.state.user.user_id)