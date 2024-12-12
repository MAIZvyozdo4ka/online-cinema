from fastapi import APIRouter, Request, Path
from fastapi.responses import StreamingResponse, HTMLResponse
from typing import Annotated
from core.schemas import MovieID
from .schemas import MovieOut
from .dao import MovieDAO, MovieS3DAO
from .errors import MovieHTTPException
from fastapi.templating import Jinja2Templates
from core.services_and_endpoints import endpoints




templates = Jinja2Templates(directory='./app/templates')

router = APIRouter(prefix = '/movie/{movie_id}',
                   tags = ['Фильмы'],
                   responses = MovieHTTPException.get_responses_schemas()
                )




@router.get(path = '', summary = 'Поиск фильма по ID')
async def get_movie_by_id(request : Request, movie_id : Annotated[MovieID, Path()]) -> MovieOut:
    return await MovieDAO.get_movie_by_id(movie_id)


@router.get(path = '/play', summary = 'Видеоконтент')
async def get_video_by_id(movie_id : Annotated[MovieID, Path()])-> StreamingResponse:
    return await MovieS3DAO.get_movie_video(movie_id = movie_id)


@router.get('/js-video')
async def play_video(request: Request, movie_id : Annotated[MovieID, Path()]) -> HTMLResponse:
    """
        Удалить - пример фронта
    """
    return templates.TemplateResponse(
        'play_videojs.html', {'request': request, 'video': {'link': f'{endpoints.MOVIE_ENDPOINT}/{movie_id}/play'}}
    )