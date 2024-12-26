from tests.Base import TestBase
from admin_service.app.set_role.dao import SetRoleDAO
from admin_service.app.set_role.schemas import UserNewRoleIn
from admin_service.app.set_role.errors import SetRoleException, SetRoleErrorType
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from core.models.postgres import UserRole, UserDB
from core.dependencies.JWTToken import IssuedJWTTokensOut
from fastapi import Request





class TestAdminSetRole(TestBase):
    
    
    
    @staticmethod
    async def test_set_role(session : AsyncSession, get_user_request : tuple[dict[str, str], int, IssuedJWTTokensOut]):
        await SetRoleDAO.set_role(session, UserNewRoleIn(user_id = get_user_request[1], role = UserRole.moderator))
        user = await session.get(UserDB, get_user_request[1])
        assert user.role == UserRole.moderator
        

    @staticmethod
    async def test_set_semi_role(session : AsyncSession, get_user_request : tuple[dict[str, str], int, IssuedJWTTokensOut]):
        
        with pytest.raises(SetRoleException) as error:
            await SetRoleDAO.set_role(session, UserNewRoleIn(user_id = get_user_request[1], role = UserRole.user))
            
        assert error.value.detail['ditail']['type'] == SetRoleErrorType.USER_HAVE_ROLE
        
        
    @staticmethod
    async def test_set_role_for_incorrect_user(session : AsyncSession, get_user_request : tuple[dict[str, str], int, IssuedJWTTokensOut]):
        
        with pytest.raises(SetRoleException) as error:
            await SetRoleDAO.set_role(session, UserNewRoleIn(user_id = get_user_request[1] + 1, role = UserRole.user))
            
        assert error.value.detail['ditail']['type'] == SetRoleErrorType.USER_NOT_FOUND
        
        
    @staticmethod
    async def test_set_role_for_admin(session : AsyncSession, get_user_request : tuple[dict[str, str], int, IssuedJWTTokensOut]):
        await SetRoleDAO.set_role(session, UserNewRoleIn(user_id = get_user_request[1], role = UserRole.admin))
        
        with pytest.raises(SetRoleException) as error:
            await SetRoleDAO.set_role(session, UserNewRoleIn(user_id = get_user_request[1], role = UserRole.user))
            
        assert error.value.detail['ditail']['type'] == SetRoleErrorType.IS_ADMIN
        