from fastapi import APIRouter, Depends, Request
from core.schemas import PrivateUserInfoOut
from fastapi.responses import RedirectResponse
from .dao import UserAccountDAO
from core.dependencies.JWTToken import JWTException, TokenValidation
from core.services_and_endpoints import servicesurls, endpoints



router = APIRouter(
                   tags = ['Пользовательский аккаунт'],
                   dependencies = [Depends(TokenValidation.check_access_token)],
                   responses = JWTException.get_responses_schemas()
                )



@router.get(path = '/account', summary = 'Информация о пользователе')
async def user_account(request : Request) -> PrivateUserInfoOut:
    return await UserAccountDAO.get_user_by_user_id(user_id = request.state.user.user_id)
    
    
    
@router.get(path = '/logout', summary = 'Выход из аккаунта')
async def logout(request : Request) -> str:
    await UserAccountDAO.logout(request.state.user.device_id)
    return endpoints.LOGIN_ENDPOINT



@router.get(path = '/full-logout', summary = 'Выход из аккаунта со всех устройств')
async def full_logout(request : Request) -> str:
    await UserAccountDAO.full_logout(request.state.user.user_id)
    return endpoints.LOGIN_ENDPOINT
