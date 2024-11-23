from app.database import IssuedJWTTokenDB
from .schemas import IssuedJWTTokensOut
from .errors import TokenRevokedError, JWTExeption
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from .JWTToken import JWTToken
from app.BaseDAO import BaseDAO, AsyncSession
from app.user.schemas import PrivateUserInfoOut


class JWTTokenDAO(BaseDAO):
    
    
    @classmethod
    @BaseDAO.get_session()
    async def check_token_is_remove(cls, session : AsyncSession, jti : int) -> None:
        token_db = await session.get(IssuedJWTTokenDB, jti)
        
        if token_db is None:
            raise TokenRevokedError
    
        
        
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
        
        
        
    @classmethod
    def generate_and_save_new_tokens_by_user_id(cls,
                                                session : AsyncSession,
                                                payload : PrivateUserInfoOut,
                                            ) -> IssuedJWTTokensOut:
        new_tokens_with_data = JWTToken.generate_tokens(payload)
        new_tokens_db = [IssuedJWTTokenDB(**token_data.model_dump(exclude = {'role', 'username'})) for token_data in new_tokens_with_data.data]
        session.add_all(new_tokens_db)
        return new_tokens_with_data.tokens
        
    
        
    
        
        
             
            