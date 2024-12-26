from fastapi import APIRouter, Request, Depends, Path
from core.schemas import MovieID, UserActionOut, SuccessUserActionStatusType
from .schemas import NewMovieIn, UpdateMoiveIn
from .dao import AdminMovieDAO
from core.services_and_endpoints import endpoints
from .errors import MovieActionException
from typing import Annotated



router = APIRouter(
                    prefix = '/moive',
                    tags = ['Добавление удаление и изменение фильмов'], 
                    responses = MovieActionException.get_responses_schemas()
                )



@router.put('', summary = 'Добавление нового фильма')
async def create_new_moive(movie : NewMovieIn) -> str:
    movie_id = await AdminMovieDAO.insert_new_movie(movie)
    return f'{endpoints.MOVIE_ENDPOINT}/{movie_id}'



@router.post('', summary = 'Обновление фильма')
async def update_moive(movie : UpdateMoiveIn) -> str:
    await AdminMovieDAO.update_movie(movie)
    return f'{endpoints.MOVIE_ENDPOINT}/{movie.id}'



@router.delete('/{movie_id}', summary = 'Удаление фильма')
async def delete_moive(movie_id : Annotated[MovieID, Path()]) -> UserActionOut:
    await AdminMovieDAO.delete_movie(movie_id)
    return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_DELETE)

