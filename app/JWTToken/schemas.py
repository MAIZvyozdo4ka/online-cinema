from pydantic import Field, ConfigDict, EmailStr, AliasChoices
from uuid import UUID, uuid4
from BaseSchema import Model



class UserOut(Model):
    
    user_id : int = Field(validation_alias = AliasChoices('id', 'user_id'))
    first_name : str = Field(description = 'Имя пользователя')
    last_name : str = Field(description = 'Фамилия пользователя')
    username : str = Field(description = 'Ник пользователя')
    is_admin : bool = Field(exclude = True)
    email : EmailStr = Field(description = 'Почта пользователя')
    
    model_config = ConfigDict(title = 'Информация о пользователе')
    
    

class IssuedJWTTokenData(Model):
    
    user_id : int = Field(description = 'ID пользователя')
    jti : UUID = Field(description = 'UUID токена', default_factory = uuid4)
    device_id : str = Field(validation_alias = AliasChoices('device_id', 'sub'), description = 'Индификатор устройства')
    
    model_config = ConfigDict(title = 'Информация о токене')
    
    
    
class IssuedJWTTokensOut(Model):
    
    access_token : str = Field(description = 'access_token')
    refresh_token : str = Field(description = 'refresh_token')
    
    model_config = ConfigDict(title = 'Сгенерированые access_token и refresh_token')
    
    
    
class IssuedJWTTokensWithDataOut(Model):
    
    tokens : IssuedJWTTokensOut
    data : tuple[IssuedJWTTokenData, IssuedJWTTokenData] 
    
    
    

    