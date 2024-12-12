from fastapi import APIRouter
from .schemas import UserRegistrationCredentialsIn, UserLoginCredentialsIn, RefreshTokenIn
from .dao import AuthDAO
from .errors import AuthExeption
from core.dependencies.JWTToken import IssuedJWTTokensOut, JWTExeption




router = APIRouter(tags = ['Аунтификация'],
                   responses = AuthExeption.get_responses_schemas()
                )


@router.post(path = '/registration', summary = 'Регистация пользователя')
async def registrate(user_credentials : UserRegistrationCredentialsIn) -> IssuedJWTTokensOut:
    return await AuthDAO.registrate(user_credentials)


@router.post(path = '/login', summary = 'Вход в аккаунт')
async def login(user_credentials : UserLoginCredentialsIn) -> IssuedJWTTokensOut:
    return await AuthDAO.login(user_credentials)


@router.post(path = '/update-tokens', summary = 'Обновление токенов', responses = JWTExeption.get_responses_schemas())
async def update_tokens(user_credentials : RefreshTokenIn) -> IssuedJWTTokensOut:
    return await AuthDAO.update_tokens(user_credentials)



    
