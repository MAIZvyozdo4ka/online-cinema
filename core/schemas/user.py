from pydantic import Field, ConfigDict, EmailStr, AliasChoices
from .BaseModel import BaseModel
from core.models.postgres import UserRole


class NonPrivateUserInfo(BaseModel):
    username : str = Field(min_length = 4, max_length = 50, description = 'Ник пользователя')
    
    model_config = ConfigDict(title = 'Короткая инормация о пользователе')
 

class PrivateUserInfo(NonPrivateUserInfo):
    first_name : str = Field(min_length = 1, max_length = 50, xdescription = 'Имя пользователя')
    last_name : str = Field(min_length = 1, max_length = 50, description = 'Фамилия пользователя')
    email : EmailStr = Field(min_length = 1, max_length = 50, description = 'Почта пользователя')   
    

class NonPrivateUserInfoOut(NonPrivateUserInfo):
    role : UserRole = Field(default = UserRole.user)
    user_id : int = Field(validation_alias = AliasChoices('id', 'user_id'))
    



class PrivateUserInfoOut(NonPrivateUserInfoOut, PrivateUserInfo):
    pass
    