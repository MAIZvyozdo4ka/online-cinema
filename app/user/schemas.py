from pydantic import Field, ConfigDict, EmailStr, AliasChoices
from app.BaseModel import BaseModel
from app.database import UserRole


class NonPrivateUserInfo(BaseModel):
    username : str = Field(min_length = 4, description = 'Ник пользователя')
    
    model_config = ConfigDict(title = 'Короткая инормация о пользователе')
    
    

class NonPrivateUserInfoOut(NonPrivateUserInfo):
    role : UserRole = Field(default = UserRole.user)
    user_id : int = Field(validation_alias = AliasChoices('id', 'user_id'))
    
    

class PrivateUserInfo(NonPrivateUserInfo):
    first_name : str = Field(min_length = 1, description = 'Имя пользователя')
    last_name : str = Field(min_length = 1,description = 'Фамилия пользователя')
    email : EmailStr = Field(description = 'Почта пользователя')


class PrivateUserInfoOut(NonPrivateUserInfoOut, PrivateUserInfo):
    pass
    
 
