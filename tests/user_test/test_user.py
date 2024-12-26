from tests.Base import TestBase
from auth_service.app.auth.dao import AuthDAO
from auth_service.app.auth.schemas import UserLoginCredentialsIn
from core.dependencies.JWTToken import TokenValidation, JWTException, AccessErrorType, IssuedJWTTokensOut
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.app.account.dao import UserAccountDAO
import pytest
from tests.Base import fixture
from fastapi import Request





class TestUserAccount(TestBase):
    
    
    @staticmethod
    async def test_account(session : AsyncSession, get_user_request : tuple[dict[str, str], int, IssuedJWTTokensOut]) -> None:
        user_info = await UserAccountDAO.get_user_by_user_id(session, get_user_request[1])
        assert get_user_request[0]['username'] == user_info.username
        assert get_user_request[0]['email'] == user_info.email
        assert get_user_request[0]['first_name'] == user_info.first_name
        assert get_user_request[0]['last_name'] == user_info.last_name
        
    
    @staticmethod
    async def test_logout(session : AsyncSession, user_registrate :  tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        tokens = await AuthDAO.login(session, UserLoginCredentialsIn(
                                                            password = user_registrate[0]['password'], 
                                                            username_or_email = user_registrate[0]['email']
                                                        )
                                                    )
        req = Request(scope = {'type' : 'http'})
        await TokenValidation.check_accsess_token_with_session(req, f'Bearer {tokens.access_token}', session)
        await UserAccountDAO.logout(session, req.state.user.device_id)
        with pytest.raises(JWTException) as error:
            await TokenValidation.check_accsess_token_with_session(Request(scope = {'type' : 'http'}), f'Bearer {tokens.access_token}', session)
            
        await TokenValidation.check_accsess_token_with_session(Request(scope = {'type' : 'http'}), f'Bearer {user_registrate[1].access_token}', session)
        assert error.value.detail['ditail']['type'] == AccessErrorType.TOKEN_REVOKED
    
    
    
    @staticmethod
    async def test_full_logout(session : AsyncSession, get_user_request :  tuple[dict[str, str], int, IssuedJWTTokensOut]) -> None:
        tokens = await AuthDAO.login(session, UserLoginCredentialsIn(
                                                            password = get_user_request[0]['password'], 
                                                            username_or_email = get_user_request[0]['email']
                                                        )
                                                    )
        await TokenValidation.check_accsess_token_with_session(Request(scope = {'type' : 'http'}), f'Bearer {tokens.access_token}', session)
        await UserAccountDAO.full_logout(session, get_user_request[1])
        with pytest.raises(JWTException) as error:
            await TokenValidation.check_accsess_token_with_session(Request(scope = {'type' : 'http'}), f'Bearer {get_user_request[2].access_token}', session)
        assert error.value.detail['ditail']['type'] == AccessErrorType.TOKEN_REVOKED
        with pytest.raises(JWTException) as new_tokens_error:
            await TokenValidation.check_accsess_token_with_session(Request(scope = {'type' : 'http'}), f'Bearer {tokens.access_token}', session)
        assert new_tokens_error.value.detail['ditail']['type'] == AccessErrorType.TOKEN_REVOKED
           
        