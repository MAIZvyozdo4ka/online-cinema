from tests.Base import TestBase
from auth_service.app.auth.dao import AuthDAO
from auth_service.app.auth.schemas import UserLoginCredentialsIn, UserRegistrationCredentialsIn
from core.dependencies.JWTToken import IssuedJWTTokensOut
from auth_service.app.auth.errors import AuthException, AuthErrorType
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from tests.Base import fixture


        






class TestLogin(TestBase):
    
    
    
    @staticmethod
    async def test_correct_login_by_email(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        login_data = UserLoginCredentialsIn(username_or_email = user_registrate[0]['email'], password = user_registrate[0]['password'])
        await AuthDAO.login(session, login_data)
        
    @staticmethod
    async def test_correct_login_by_username(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        login_data = UserLoginCredentialsIn(username_or_email = user_registrate[0]['username'], password = user_registrate[0]['password'])
        await AuthDAO.login(session, login_data)
        
    
    @staticmethod
    async def test_incorrect_password_login(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        login_data = UserLoginCredentialsIn(username_or_email = user_registrate[0]['username'], password = 'incorrect_password')
        
        with pytest.raises(AuthException) as error:
            await AuthDAO.login(session, login_data)

        assert login_data.password != user_registrate[0]['password']
        assert error.value.detail['ditail']['type'] == AuthErrorType.INVALID_PASSWORD
        
    @staticmethod
    async def test_incorrect_email_login(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        login_data = UserLoginCredentialsIn(username_or_email = user_registrate[0]['email'] + '.', password = user_registrate[0]['password'])
        with pytest.raises(AuthException) as error:
            await AuthDAO.login(session, login_data)

        assert login_data.username_or_email != user_registrate[0]['email']
        assert error.value.detail['ditail']['type'] == AuthErrorType.INVALID_USERNAME_OR_EMAIL
        
        
    @staticmethod
    async def test_incorrect_username_login(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        login_data = UserLoginCredentialsIn(username_or_email = user_registrate[0]['username'] + '.', password = user_registrate[0]['password'])
        with pytest.raises(AuthException) as error:
            await AuthDAO.login(session, login_data)

        assert login_data.username_or_email != user_registrate[0]['username']
        assert error.value.detail['ditail']['type'] == AuthErrorType.INVALID_USERNAME_OR_EMAIL
        
        
    @staticmethod
    async def test_correct_many_login(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        login_data = UserLoginCredentialsIn(username_or_email = user_registrate[0]['email'], password = user_registrate[0]['password'])
        tokens1 = await AuthDAO.login(session, login_data)
        tokens2 = await AuthDAO.login(session, login_data)
        tokens3 = await AuthDAO.login(session, login_data)
        assert tokens1.access_token != tokens2.access_token
        assert tokens1.access_token != tokens3.access_token
        assert tokens2.access_token != tokens3.access_token
        assert tokens1.refresh_token != tokens2.refresh_token
        assert tokens1.refresh_token != tokens3.refresh_token
        assert tokens2.refresh_token != tokens3.refresh_token