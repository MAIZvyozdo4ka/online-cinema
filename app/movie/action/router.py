from fastapi import APIRouter, Request, Path, Depends
from typing import Annotated
from pydantic import PositiveInt
from .schemas import MovieWithUserInfoOut, MovieRatingOut, ReviewMovieWithUserInfoListWithStatisticOut
from .dao import MovieDAO
from .errors import MovieHTTPExeption
from app.JWTToken import TokenValidation



router = APIRouter(prefix = '/movie/{movie_id}',
                   tags = ['Фильмы'],
                   responses = MovieHTTPExeption.get_responses_schemas()
                )




@router.get(path = '', summary = 'Поиск фильма по ID', dependencies = [Depends(TokenValidation.weak_check_access_token)])
async def get_movie_by_id(request : Request, movie_id : Annotated[PositiveInt, Path(le = 10_000_000)]) -> MovieWithUserInfoOut:
    user_id : int | None = None
    if request.state.user is not None:
        user_id = request.state.user.user_id
    return await MovieDAO.get_movie_by_id(movie_id, request.state.user.user_id if request.state.user is not None else None)




@router.get(path = '/ratings', summary = 'Оценки фильма')
async def get_movie_retings_by_id(movie_id : Annotated[PositiveInt, Path(le = 10_000_000)]) -> list[MovieRatingOut]:

    return await MovieDAO.get_movie_rating_by_id(movie_id)


@router.get(path = '/reviews', summary = 'Рецензии фильма')
async def get_movie_reviews_by_id(movie_id : Annotated[PositiveInt, Path(le = 10_000_000)]) -> ReviewMovieWithUserInfoListWithStatisticOut:

    return await MovieDAO.get_movie_reviews_with_statistic(movie_id)