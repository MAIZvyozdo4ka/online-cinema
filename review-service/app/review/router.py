from fastapi import APIRouter, Request, Depends
from .dao import ReviewDAO
from .errors import ReviewExeption
from .schemas import ReviewMovieOut, ReviewMovieIn, DeleteReviewMovieIn, ShowUserMovieReviewsListOut
from core.dependencies.JWTToken import TokenValidation, JWTExeption

router = APIRouter(
                    dependencies = [Depends(TokenValidation.check_access_token)],
                    tags = ['Отзыв фильма'],
                    responses = ReviewExeption.get_responses_schemas() | JWTExeption.get_responses_schemas()
                )


@router.post(path = '/review-movie', summary = 'Оставить отзыв фильму')
async def review_movie(request : Request, review : ReviewMovieIn) -> ReviewMovieOut:
    review._user_id = request.state.user.user_id
    
    return await ReviewDAO.review_movie(review)



@router.delete(path = '/review-movie', summary = 'Удалить отзыв фильма')
async def review_movie(request : Request, review : DeleteReviewMovieIn) -> ReviewMovieOut:
    review._user_id = request.state.user.user_id
    
    return await ReviewDAO.delete_review_movie(review)



@router.get(path = '/my', summary = 'Рецензии фильмов пользователя')
async def user_movies_reviews(request : Request) -> ShowUserMovieReviewsListOut:
    
    return await ReviewDAO.get_user_movies_reviews(user_id = request.state.user.user_id)
