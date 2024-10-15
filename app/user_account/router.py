from fastapi import APIRouter, Body, Request, Depends
from JWTToken import JWTExeption, TokenValidation, token_schemas
from fastapi.responses import RedirectResponse
from .dao import UserAccountDAO


router = APIRouter(prefix = '/me',
                   tags = ['Пользовательский аккаунт'],
                   responses = JWTExeption.get_responses_schemas(),
                   dependencies = [Depends(TokenValidation.check_access_token_after_weak_check)] 
                )



@router.get(path = '', summary = 'Пользовательский аккаунт')
async def user_account(request : Request) -> token_schemas.UserOut:
    return request.state.user
    
    
    
@router.get(path = '/logout', summary = 'Выход из аккаунта')
async def logout(request : Request) -> RedirectResponse:
    await UserAccountDAO.logout(request.state.device_id)
    return RedirectResponse('/auth/login')



@router.get(path = '/full-logout', summary = 'Выход из аккаунта со всех устройств')
async def full_logout(request : Request) -> RedirectResponse:
    await UserAccountDAO.full_logout(request.state.user.user_id)
    return RedirectResponse('/auth/login')

