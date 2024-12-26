from tests.Base import TestBase
from auth_service.app.auth.dao import AuthDAO
from auth_service.app.auth.schemas import RefreshTokenIn
from core.dependencies.JWTToken import IssuedJWTTokensOut, JWTException, AccessErrorType
from auth_service.app.auth.errors import AuthException, AuthErrorType
from sqlalchemy.ext.asyncio import AsyncSession
import pytest




class TestUpdateTokens(TestBase):
    
    
    @staticmethod
    async def test_correct_update_tokens(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        new_tokens = await AuthDAO.update_tokens(session, RefreshTokenIn(refresh_token = user_registrate[1].refresh_token))
        assert new_tokens.access_token != user_registrate[1].access_token
       
       
    @staticmethod
    async def test_incorrect_update_tokens(session : AsyncSession) -> None:
        with pytest.raises(JWTException) as error:
            await AuthDAO.update_tokens(session, RefreshTokenIn(refresh_token = '111')) 
            
        assert error.value.detail['ditail']['type'] == AccessErrorType.INVALID_TOKEN
        
        
    @staticmethod
    async def test_second_update_tokens_with_same_refresh(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        await AuthDAO.update_tokens(session, RefreshTokenIn(refresh_token = user_registrate[1].refresh_token))
        with pytest.raises(JWTException) as error:
            await AuthDAO.update_tokens(session, RefreshTokenIn(refresh_token = user_registrate[1].refresh_token)) 
            
        assert error.value.detail['ditail']['type'] == AccessErrorType.TOKEN_REVOKED
       