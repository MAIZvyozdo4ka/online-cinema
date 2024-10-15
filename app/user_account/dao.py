from database import async_session_maker, UserDB, IssuedJWTTokenDB
from JWTToken import JWTTokenDAO


class UserAccountDAO:
    
    
    @classmethod
    async def logout(cls, device_id : str) -> None:
        async with async_session_maker() as session, session.begin():
            
            await JWTTokenDAO.delete_user_tokens_by_device_id(session, device_id)
            
            
    @classmethod
    async def full_logout(cls, user_id : int) -> None:
        async with async_session_maker() as session, session.begin():
            
            await JWTTokenDAO.delete_all_user_tokens_by_user_id(session, user_id)
        
                
            
            
            