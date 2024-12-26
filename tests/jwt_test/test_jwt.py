from core.dependencies.JWTToken import IssuedJWTTokensOut, TokenValidation, JWTException, AccessErrorType
from sqlalchemy.ext.asyncio import AsyncSession
from tests.Base import TestBase
from fastapi import Request
import pytest



class TestJWT(TestBase):
    
    
    @staticmethod
    async def test_empty_token_data(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        request = Request(scope = {'type' : 'http'})
        with pytest.raises(JWTException) as error:
            await TokenValidation.check_accsess_token_with_session(request, None, session)
        assert error.value.detail['ditail']['type'] == AccessErrorType.TOKEN_IS_NOT_SPECIFIED
        
    
    @staticmethod
    async def test_token_header_bearer(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        request = Request(scope = {'type' : 'http'})
        with pytest.raises(JWTException) as error:
            await TokenValidation.check_accsess_token_with_session(request, f'{user_registrate[1].access_token}', session)
        assert error.value.detail['ditail']['type'] == AccessErrorType.INCORRECT_AUTH_HEADER_FORM
        
    
    @staticmethod
    async def test_token_invalid(session : AsyncSession, user_registrate : tuple[dict[str, str], IssuedJWTTokensOut]) -> None:
        request = Request(scope = {'type' : 'http'})
        with pytest.raises(JWTException) as error:
            await TokenValidation.check_accsess_token_with_session(request, f'Bearer {user_registrate[1].access_token}++', session)
        assert error.value.detail['ditail']['type'] == AccessErrorType.INVALID_TOKEN
        