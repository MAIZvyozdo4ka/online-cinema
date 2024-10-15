from .schemas import UserRegistrationCredentialsIn, UserLoginCredentialsIn, RefreshTokenIn
from database import async_session_maker, UserDB, IssuedJWTTokenDB
from JWTToken import JWTToken, token_schemas, TokenValidation, JWTTokenDAO
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from .errors import (
                    UsernameOccupiedError,
                    EmailOccupiedError,
                    AuthExeption,
                    InvalidPasswordError,
                    InvalidUsernameOrEmailError
                )






class AuthDAO:
    
    @classmethod
    async def get_user_by_email_or_username(cls,
                                            session : AsyncSession,
                                            username : str,
                                            email : str
                                        ) -> UserDB | None:
        
        query_for_find_user = select(UserDB).where(
                                or_(UserDB.email == email, 
                                    UserDB.username == username
                                )
                            )
        
        return await session.scalar(query_for_find_user)
      
          
    
    @classmethod
    async def get_user_with_same_credentials(cls,
                                               session : AsyncSession,
                                               user_credentials : UserRegistrationCredentialsIn
                                            ) -> AuthExeption | None:
        
        user_with_same_credentials = await cls.get_user_by_email_or_username(session, user_credentials.username, user_credentials.email)

        if user_with_same_credentials is None:
            return None
        
        if user_credentials.email == user_with_same_credentials.email:
            return EmailOccupiedError
        
        return UsernameOccupiedError
    
    
    
    @classmethod
    async def get_user_with_logining_credentials(cls, 
                                                  session : AsyncSession,
                                                  user_credentials : UserLoginCredentialsIn,
                                                ) -> tuple[UserDB | None, AuthExeption | None]:
                    
        user = await cls.get_user_by_email_or_username(session, user_credentials.username_or_email, user_credentials.username_or_email)
        
        if user is None:
            return None, InvalidUsernameOrEmailError
        
        if user.hash_password != UserLoginCredentialsIn.password_serialize(user_credentials.password):
            return None, InvalidPasswordError
        
        return user, None
    
    
    
    @classmethod
    async def registrate(cls, user_credentials : UserRegistrationCredentialsIn) -> token_schemas.IssuedJWTTokensOut:
        
        async with async_session_maker() as session, session.begin():
            
            error = await cls.get_user_with_same_credentials(session, user_credentials)
            
            if error is not None:
                raise error
            
            new_user = UserDB(**user_credentials.model_dump())
            session.add(new_user)
            await session.flush()
            
            return cls.generate_and_save_new_tokens_by_user_id(session, new_user.id)
    
    
    
    @classmethod
    async def login(cls, user_credentials : UserLoginCredentialsIn) -> token_schemas.IssuedJWTTokensOut:
        async with async_session_maker() as session, session.begin():
            
            loggining_user, error = await cls.get_user_with_logining_credentials(session, user_credentials)
            
            if error is not None:
                raise error
            
            return cls.generate_and_save_new_tokens_by_user_id(session, loggining_user.id)
            
            
    
    @classmethod
    async def update_tokens(cls, refresh_token : RefreshTokenIn) -> token_schemas.IssuedJWTTokensOut:
        refresh_token_data = TokenValidation.check_refresh_token(refresh_token.refresh_token)
        
        async with async_session_maker() as session, session.begin():
            
            user_id, error = await JWTTokenDAO.delete_user_tokens_by_device_id(session, refresh_token_data.device_id)
            
            if error is None:
                return cls.generate_and_save_new_tokens_by_user_id(session, user_id)
            
            await JWTTokenDAO.delete_all_user_tokens_by_user_id(session, refresh_token_data.user_id)
            
        raise error
            
                                  
      
      
    @classmethod
    def generate_and_save_new_tokens_by_user_id(cls,
                                                session : AsyncSession,
                                                user_id : int
                                            ) -> token_schemas.IssuedJWTTokensOut:
        new_tokens_with_data = JWTToken.generate_tokens(user_id)
        new_tokens_db = [IssuedJWTTokenDB(**token_data.model_dump()) for token_data in new_tokens_with_data.data]
        session.add_all(new_tokens_db)
        return new_tokens_with_data.tokens      
    
    
        
        
            
        
        
        
            
            