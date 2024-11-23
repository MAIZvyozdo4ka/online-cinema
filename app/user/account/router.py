from fastapi import APIRouter, Body, Request
from app.user.schemas import PrivateUserInfoOut
from fastapi.responses import RedirectResponse
from .dao import UserAccountDAO
from .schemas import ShowUserMovieRatingListOut, ShowUserMovieReviewsListOut


router = APIRouter(prefix = '/me',
                   tags = ['Пользовательский аккаунт']
                )



@router.get(path = '', summary = 'Информация о пользователе')
async def user_account(request : Request) -> PrivateUserInfoOut:
    return await UserAccountDAO.get_user_by_user_id(user_id = request.state.user.user_id)
    
    
    
@router.get(path = '/logout', summary = 'Выход из аккаунта')
async def logout(request : Request) -> RedirectResponse:
    await UserAccountDAO.logout(request.state.device_id)
    return RedirectResponse('/auth/login')



@router.get(path = '/full-logout', summary = 'Выход из аккаунта со всех устройств')
async def full_logout(request : Request) -> RedirectResponse:
    await UserAccountDAO.full_logout(request.state.user.user_id)
    return RedirectResponse('/auth/login')



@router.get(path = '/movie-rating', summary = 'Оценки фильмов')
async def user_movies_rating(request : Request) -> ShowUserMovieRatingListOut:
    
    return await UserAccountDAO.get_user_movies_rating(user_id = request.state.user.user_id)



@router.get(path = '/movie-reviews', summary = 'Отзывы фильмов')
async def user_movies_reviews(request : Request) -> ShowUserMovieReviewsListOut:
    
    return await UserAccountDAO.get_user_movies_reviews(user_id = request.state.user.user_id)


