from fastapi import APIRouter, Request, Depends, Path, Query
from core.dependencies.JWTToken import TokenValidation
from pydantic import PositiveInt
from typing import Annotated
from .schemas import ReviewMovieWithUserInfoListWithStatisticOut, ReviewMovieWithUserInfoOut, ReviewMovie
from .dao import MovieRewivewDAO


router = APIRouter(prefix = '/movie/{movie_id}', tags = ['Рецензии фильма'])



@router.get(path = '', summary = 'Рецензии фильма')
async def get_movie_reviews_by_id(
                                movie_id : Annotated[PositiveInt, Path(le = 10_000_000)],
                                limit : Annotated[PositiveInt | None, Query(description = 'Максимальное число рецензий фильма')] = None
                            ) -> ReviewMovieWithUserInfoListWithStatisticOut | list[ReviewMovieWithUserInfoOut]:
    if limit is None:
        return await MovieRewivewDAO.get_movie_reviews_with_statistic(movie_id)

    return await MovieRewivewDAO.get_movie_reviews(movie_id = movie_id, limit = limit)


@router.get(path = '/my',
            summary = 'Рецензия пользователя определенного фильма',
            dependencies = [Depends(TokenValidation.weak_check_access_token)]
        )
async def get_movie_by_id(request : Request, movie_id : Annotated[PositiveInt, Path(le = 10_000_000)]) -> ReviewMovie | None:
    if request.state.user is None:
        return None
    
    return await MovieRewivewDAO.get_user_review_by_user_id(movie_id, request.state.user.user_id)