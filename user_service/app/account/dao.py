from core.models.postgres import UserDB
from core.dependencies.JWTToken import JWTTokenDAO
from core.dao import PostgresDAO, AsyncSession
from core.schemas import PrivateUserInfoOut


class UserAccountDAO(PostgresDAO):
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_user_by_user_id(cls, session : AsyncSession, user_id : int) -> PrivateUserInfoOut:
        user = await session.get(UserDB, user_id)
        
        return PrivateUserInfoOut.model_validate(user)
        
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def logout(cls, session : AsyncSession, device_id : str) -> None:
            
        await JWTTokenDAO.delete_user_tokens_by_device_id(session, device_id)
      
      
    @classmethod    
    @PostgresDAO.get_session(auto_commit = True)        
    async def full_logout(cls, session : AsyncSession, user_id : int) -> None:
            
        await JWTTokenDAO.delete_all_user_tokens_by_user_id(session, user_id)