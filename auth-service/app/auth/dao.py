from .schemas import UserRegistrationCredentialsIn, UserLoginCredentialsIn, RefreshTokenIn
from core.models.postgres import UserDB
from core.models.postgres.Recommendation import RecommedationDB
from core.dependencies.JWTToken import TokenValidation, JWTTokenDAO, IssuedJWTTokensOut
from sqlalchemy import select, or_, insert
from sqlalchemy.ext.asyncio import AsyncSession
from core.dao import PostgresDAO
from .errors import (
                    UsernameOccupiedError,
                    EmailOccupiedError,
                    AuthException,
                    InvalidPasswordError,
                    InvalidUsernameOrEmailError
                )
from core.schemas import NonPrivateUserInfoOut





class AuthDAO(PostgresDAO):
    
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
                                            ) -> AuthException | None:
        
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
                                                ) -> tuple[UserDB | None, AuthException | None]:
                    
        user = await cls.get_user_by_email_or_username(session, user_credentials.username_or_email, user_credentials.username_or_email)
        
        if user is None:
            return None, InvalidUsernameOrEmailError
        
        if user.hash_password != UserLoginCredentialsIn.password_serialize(user_credentials.password):
            return None, InvalidPasswordError
        
        return user, None
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def registrate(cls,
                         session : AsyncSession, 
                         user_credentials : UserRegistrationCredentialsIn
                        ) -> IssuedJWTTokensOut:
        query_for_new_user = insert(UserDB).values(user_credentials.model_dump()).returning(UserDB.id)
        
        error = await cls.get_user_with_same_credentials(session, user_credentials)
        
        if error is not None:
            raise error
        
        user_id = await session.scalar(query_for_new_user)

        query = insert(RecommedationDB).values(userId=user_id).returning(RecommedationDB.userId)
        await session.scalar(query)

        return JWTTokenDAO.generate_and_save_new_tokens_by_user_id(session, 
                                                                        NonPrivateUserInfoOut(
                                                                                username = user_credentials.username,
                                                                                user_id = user_id
                                                                            )
                                                                    )
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def login(cls,
                    session : AsyncSession,
                    user_credentials : UserLoginCredentialsIn
                ) -> IssuedJWTTokensOut:
            
        loggining_user, error = await cls.get_user_with_logining_credentials(session, user_credentials)
        
        if error is not None:
            raise error
        
        return JWTTokenDAO.generate_and_save_new_tokens_by_user_id(session, NonPrivateUserInfoOut.model_validate(loggining_user))
            
            
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True, ignore_http_errors = True)
    async def update_tokens(cls,
                            session : AsyncSession,
                            refresh_token : RefreshTokenIn
                        ) -> IssuedJWTTokensOut:
        refresh_token_data = TokenValidation.check_refresh_token(refresh_token.refresh_token)    
        _, error = await JWTTokenDAO.delete_user_tokens_by_device_id(session, refresh_token_data.device_id)
        
        if error is not None:
            await JWTTokenDAO.delete_all_user_tokens_by_user_id(session, refresh_token_data.user_id)
            raise error
        
        return JWTTokenDAO.generate_and_save_new_tokens_by_user_id(session, NonPrivateUserInfoOut.model_validate(refresh_token_data))
            
                                  
      
            
    
    
        
        
            
        
        
        
            
            