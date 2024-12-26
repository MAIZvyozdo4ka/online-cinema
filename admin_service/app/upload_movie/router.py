from fastapi import APIRouter, Request, Depends, Path, UploadFile
from core.schemas import MovieID, UserActionOut, SuccessUserActionStatusType
from core.services_and_endpoints import endpoints
from typing import Annotated
from .dao import MovieS3DAO
from .errors import MovieUploadException


router = APIRouter(
                    prefix = '/movie-s3/{movie_id}',
                    tags = ['Добавление удаление и изменение файлов фильма'], 
                    responses = MovieUploadException.get_responses_schemas()
                )




@router.post(path = '/upload', summary = 'Загрузка фильма')
async def upload_movie(movie_file : UploadFile, movie_id : Annotated[MovieID, Path()]) -> UserActionOut:
    await MovieS3DAO.upload_movie(movie_file, movie_id)
    return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_INSERT)
    
    
@router.delete(path = '/delete', summary = 'Удаление фильма')
async def delete_movie(movie_id : Annotated[MovieID, Path()]) -> None:
    await MovieS3DAO.delete_movie(movie_id)
