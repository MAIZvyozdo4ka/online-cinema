from fastapi import APIRouter, Request
from .schemas import RateMovieIn, DeleteRateMovieIn, RateMovieOut
from .dao import RatingDAO
from .errors import RatingExeption


router = APIRouter(
                    tags = ['Оценка фильма'], 
                    responses = RatingExeption.get_responses_schemas()
                )


@router.post(path = '/rate-movie', summary = 'Оставить оценку фильму')
async def rate_movie(request : Request, rating : RateMovieIn) -> RateMovieOut:
    rating._user_id = request.state.user.user_id
    
    return await RatingDAO.rate_movie(rating)


@router.delete(path = '/rate-movie', summary = 'Удалить оценку фильма')
async def rate_movie(request : Request, rating : DeleteRateMovieIn) -> RateMovieOut:
    rating._user_id = request.state.user.user_id
    
    return await RatingDAO.delete_rate_movie(rating)