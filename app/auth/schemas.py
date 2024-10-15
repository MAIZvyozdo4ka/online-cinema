from pydantic import Field, ConfigDict, field_serializer, EmailStr, field_validator
from BaseSchema import Model
from hashlib import sha256
from .errors import IncorrectUsernameError
import re



class UserCredentialsIn(Model):
    
    password : str = Field(serialization_alias = 'hash_password', min_length = 8, description = 'Пароль')
    
    @field_serializer('password')
    @classmethod
    def password_serialize(cls, password : str) -> str:
        return sha256(str.encode(password)).hexdigest()




class UserLoginCredentialsIn(UserCredentialsIn):
    username_or_email : str | EmailStr = Field(min_length = 8, description = 'Никнейм или емейл')
    
    model_config = ConfigDict(title = 'Вход в аккаут')
    



class UserRegistrationCredentialsIn(UserCredentialsIn):
    
    username : str = Field(min_length = 8, description = 'Никнейм')
    email : EmailStr = Field(min_length = 5, description = 'Емайл')
    first_name : str = Field(min_length = 1, description = 'Имя')
    last_name : str = Field(min_length = 1, description = 'Фамилия')
    
    model_config = ConfigDict(title = 'Создание аккаута')
    
    
    @field_validator('username', mode = 'after')
    @classmethod
    def check_username_is_not_like_email(cls, username : str) -> str:
        if re.match(r'^\S+@\S+\.\S+$', username):
            raise IncorrectUsernameError
        return username
        
        
        
        
class RefreshTokenIn(Model):
    
    refresh_token : str = Field(min_length = 1, description = 'refresh_token')
    
    model_config = ConfigDict(title = 'Форма для обновления токенов')
    
    

    

