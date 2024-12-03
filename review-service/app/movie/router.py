from fastapi import APIRouter, Request, Depends, Path, Query
from core.dependencies.JWTToken import TokenValidation
from pydantic import PositiveInt
from typing import Annotated
from .schemas import ReviewMovieWithUserInfoListWithStatisticOut, ReviewMovieWithUserInfoOut, ReviewMovie
from .dao import MovieRewivewDAO
from core.schemas import MovieID, MAX_MOVIE_ID


router = APIRouter(prefix = '/movie/{movie_id}', tags = ['Рецензии фильма'])



@router.get(path = '', summary = 'Рецензии фильма')
async def get_movie_reviews_by_id(
                                movie_id : Annotated[MovieID, Path()],
                                offset : Annotated[PositiveInt | None, Query(le = MAX_MOVIE_ID, description = 'Количество рецензий фильма, которые нужно пропустить')] = None,
                                limit : Annotated[PositiveInt | None, Query(le = MAX_MOVIE_ID, description = 'Максимальное число рецензий фильма')] = None
                            ) -> ReviewMovieWithUserInfoListWithStatisticOut | list[ReviewMovieWithUserInfoOut]:
    """
    Для того что бы получить рецензии со статистикой нужно не указывать никакие доп параметры
    """
    if limit is None and offset is None:
        return await MovieRewivewDAO.get_movie_reviews_with_statistic(movie_id)

    return await MovieRewivewDAO.get_movie_reviews(movie_id = movie_id, limit = limit, offset = offset)


@router.get(path = '/my',
            summary = 'Рецензия пользователя определенного фильма',
            dependencies = [Depends(TokenValidation.weak_check_access_token)]
        )
async def get_movie_by_id(request : Request, movie_id : Annotated[MovieID, Path()]) -> ReviewMovie | None:
    if request.state.user is None:
        return None
    
    return await MovieRewivewDAO.get_user_review_by_user_id(movie_id, request.state.user.user_id)