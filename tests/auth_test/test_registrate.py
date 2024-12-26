from tests.Base import TestBase
from auth_service.app.auth.dao import AuthDAO
from auth_service.app.auth.schemas import UserRegistrationCredentialsIn
from auth_service.app.auth.errors import AuthException, AuthErrorType
from sqlalchemy.ext.asyncio import AsyncSession
import pytest




class TestRegistration(TestBase):
    
    
    @staticmethod
    async def test_first_registrate(session : AsyncSession, test_user_data : dict[str, str]) -> None:
        
        await AuthDAO.registrate(session, UserRegistrationCredentialsIn.model_validate(test_user_data))
        
        
    @staticmethod
    async def test_registrate_with_full_same_credentials(session : AsyncSession, test_user_data : dict[str, str]) -> None:
        await AuthDAO.registrate(session, UserRegistrationCredentialsIn.model_validate(test_user_data))
        with pytest.raises(AuthException) as error:
            await AuthDAO.registrate(session, UserRegistrationCredentialsIn.model_validate(test_user_data))

        assert test_user_data['email'] == test_user_data['email']
        assert error.value.detail['ditail']['type'] == AuthErrorType.EMAIL_OCCUPIED
        
    
    @staticmethod
    async def test_registrate_with_same_username_credentials(session : AsyncSession, test_users_data : list[dict[str, str]]) -> None:
        first = test_users_data[0]
        await AuthDAO.registrate(session, UserRegistrationCredentialsIn.model_validate(first))
        
        second = test_users_data[1]
        second['username'] = first['username']
        
        with pytest.raises(AuthException) as error:
            await AuthDAO.registrate(session, UserRegistrationCredentialsIn.model_validate(second))

        assert first['username'] == second['username']
        assert error.value.detail['ditail']['type'] == AuthErrorType.USERNAME_OCCUPIED
        
    
    @staticmethod
    async def test_tree_client_registrate(session : AsyncSession, test_users_data : list[dict[str, str]]) -> None:
        
        tokens1 = await AuthDAO.registrate(session, UserRegistrationCredentialsIn.model_validate(test_users_data[0]))
        tokens2 = await AuthDAO.registrate(session, UserRegistrationCredentialsIn.model_validate(test_users_data[1]))
        tokens3 = await AuthDAO.registrate(session, UserRegistrationCredentialsIn.model_validate(test_users_data[2]))
        assert tokens1.access_token != tokens2.access_token
        assert tokens1.access_token != tokens3.access_token
        assert tokens2.access_token != tokens3.access_token
        assert tokens1.refresh_token != tokens2.refresh_token
        assert tokens1.refresh_token != tokens3.refresh_token
        assert tokens2.refresh_token != tokens3.refresh_token
        