from database import IssuedJWTTokenDB, async_session_maker
from .schemas import UserOut
from .errors import TokenRevokedError, JWTExeption
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete



class JWTTokenDAO:
    
    
    @classmethod
    async def get_user_by_jti(cls, jti : str) -> UserOut:
        
        async with async_session_maker() as session:
            token_db = await session.get(IssuedJWTTokenDB, jti)
            
            if token_db is None:
                raise TokenRevokedError
            
            return UserOut.model_validate(token_db.subject)
        
        
    @classmethod
    async def delete_user_tokens_by_device_id(
                                            cls,
                                            session : AsyncSession,
                                            device_id : str
                                        ) -> tuple[int | None, JWTExeption | None]:
        query_for_delete_tokens = delete(IssuedJWTTokenDB).where(
                                            IssuedJWTTokenDB.device_id == device_id
                                        ).returning(IssuedJWTTokenDB.user_id)
        
        user_id = await session.scalar(query_for_delete_tokens)
        
        if not user_id:
            return None, TokenRevokedError
        
        return user_id, None
    
    
    @classmethod
    async def delete_all_user_tokens_by_user_id(cls,
                                                session : AsyncSession,
                                                user_id : int
                                            ) -> None:
        query_for_delete_all_tokens = delete(IssuedJWTTokenDB).where(
                                        IssuedJWTTokenDB.user_id == user_id
                                    )
        await session.execute(query_for_delete_all_tokens)
        
    
        
    
        
        
             
            