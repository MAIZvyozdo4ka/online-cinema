from fastapi import APIRouter, Query, Request, Depends
from typing import Annotated
from .schemas import MoviePreviewOut
from .dao import RecDAO
from .errors import RecHTTPException
from core.dependencies.JWTToken import TokenValidation, JWTException



router = APIRouter(tags = ['Рекоммендации'],
                   dependencies=[Depends(TokenValidation.check_access_token)],
                   responses=JWTException.get_responses_schemas() | RecHTTPException.get_responses_schemas(),
                   )



@router.get(path = '/recommendation', summary = 'Рекоммендации фильмов')
async def recommendation(request : Request) -> list[MoviePreviewOut]:

    return await RecDAO.recommendation_by_user_id(user_id = request.state.user.user_id)



    