from fastapi import APIRouter, Request, Depends, Path
from .schemas import RateMovieIn, DeleteRateMovieIn, RateMovieOut, ShowUserMovieRatingListOut, RateMovie
from .dao import RatingDAO
from .errors import RatingExeption
from core.dependencies.JWTToken import TokenValidation, JWTExeption


router = APIRouter(
                    tags = ['Оценка фильмов'], 
                    dependencies = [Depends(TokenValidation.check_access_token)],
                    responses = JWTExeption.get_responses_schemas() | RatingExeption.get_responses_schemas()
                )


@router.post(path = '/rate-movie', summary = 'Оставить оценку фильму')
async def rate_movie(request : Request, rating : RateMovieIn) -> RateMovieOut:
    rating._user_id = request.state.user.user_id
    
    return await RatingDAO.rate_movie(rating)



@router.delete(path = '/rate-movie', summary = 'Удалить оценку фильма')
async def delete_rate_movie(request : Request, rating : DeleteRateMovieIn) -> RateMovieOut:
    rating._user_id = request.state.user.user_id
    
    return await RatingDAO.delete_rate_movie(rating)



@router.get(path = '/my', summary = 'Оценки фильмов пользователя')
async def user_movies_rating(request : Request) -> ShowUserMovieRatingListOut:
    
    return await RatingDAO.get_user_movies_rating(user_id = request.state.user.user_id)
