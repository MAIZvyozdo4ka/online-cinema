from fastapi import APIRouter, Request
from .dao import ReviewDAO
from .errors import ReviewException
from .schemas import ReviewMovieOut, ReviewMovieIn, DeleteReviewMovieIn


router = APIRouter(
                    tags = ['Отзыв фильма'],
                    responses = ReviewException.get_responses_schemas()
                )


@router.post(path = '/review-movie', summary = 'Оставить отзыв фильму')
async def review_movie(request : Request, review : ReviewMovieIn) -> ReviewMovieOut:
    review._user_id = request.state.user.user_id
    
    return await ReviewDAO.review_movie(review)


@router.delete(path = '/review-movie', summary = 'Удалить отзыв фильма')
async def review_movie(request : Request, review : DeleteReviewMovieIn) -> ReviewMovieOut:
    review._user_id = request.state.user.user_id
    
    return await ReviewDAO.delete_review_movie(review)