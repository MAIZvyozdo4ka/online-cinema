from fastapi import APIRouter
from .schemas import UserRegistrationCredentialsIn, UserLoginCredentialsIn, RefreshTokenIn
from .dao import AuthDAO
from .errors import AuthExeption
from app.JWTToken import IssuedJWTTokensOut, JWTExeption




router = APIRouter(prefix = '/auth',
                   tags = ['Аунтификация'],
                   responses = AuthExeption.get_responses_schemas()
                )



@router.get(path = '/registration', summary = 'HTML страничка с формой регистрации')
async def show_registration_html() -> str:
    return 'this is reg html'



@router.post(path = '/registration', summary = 'Регистация пользователя')
async def registrate(user_credentials : UserRegistrationCredentialsIn) -> IssuedJWTTokensOut:
    return await AuthDAO.registrate(user_credentials)



@router.get(path = '/login', summary = 'HTML страничка с формой логина')
async def show_login_html() -> str:
    return 'this is login html'



@router.post(path = '/login', summary = 'Вход в аккаунт')
async def login(user_credentials : UserLoginCredentialsIn) -> IssuedJWTTokensOut:
    return await AuthDAO.login(user_credentials)



@router.post(path = '/update-tokens', summary = 'Обновление токенов', responses = JWTExeption.get_responses_schemas())
async def update_tokens(user_credentials : RefreshTokenIn) -> IssuedJWTTokensOut:
    return await AuthDAO.update_tokens(user_credentials)



    
