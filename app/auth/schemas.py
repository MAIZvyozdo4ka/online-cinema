from pydantic import Field, ConfigDict, field_serializer, EmailStr, field_validator
from app.BaseModel import BaseModel
from hashlib import sha256
import re
from app.user.schemas import PrivateUserInfo



class UserCredentialsIn(BaseModel):
    
    password : str = Field(serialization_alias = 'hash_password', min_length = 5, description = 'Пароль')
    
    @field_serializer('password')
    @classmethod
    def password_serialize(cls, password : str) -> str:
        return sha256(str.encode(password)).hexdigest()




class UserLoginCredentialsIn(UserCredentialsIn):
    username_or_email : str | EmailStr = Field(min_length = 5, description = 'Никнейм или емейл')
    
    model_config = ConfigDict(title = 'Вход в аккаут')
    



class UserRegistrationCredentialsIn(PrivateUserInfo, UserCredentialsIn):
    
    model_config = ConfigDict(title = 'Создание аккаута')
    
    
    @field_validator('username', mode = 'after')
    @classmethod
    def check_username_is_not_like_email(cls, username : str) -> str:
        if re.match(r'^\S+@\S+\.\S+$', username):
            raise ValueError('username like email')
        return username
        
        
        
        
class RefreshTokenIn(BaseModel):
    
    refresh_token : str = Field(min_length = 1, description = 'refresh_token')
    
    model_config = ConfigDict(title = 'Форма для обновления токенов')
    
    

    

