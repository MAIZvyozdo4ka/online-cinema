from pydantic import Field, ConfigDict, AliasChoices
from uuid import UUID, uuid4
from app.BaseModel import BaseModel
from .config import jwtsettings
from app.user.schemas import NonPrivateUserInfoOut



class IssuedJWTTokenData(NonPrivateUserInfoOut):
    
    jti : UUID = Field(description = 'UUID токена', default_factory = uuid4)
    device_id : str = Field(description = 'Индификатор устройства')
    
    model_config = ConfigDict(title = 'Информация о токене')
    
    
    
class IssuedJWTTokensOut(BaseModel):
    
    access_token : str = Field(description = 'access_token')
    refresh_token : str = Field(description = 'refresh_token')
    exp : float = Field(default = jwtsettings.ACCESS_TOKEN_TTL.total_seconds(), description = 'Время жизни access_token')
    
    model_config = ConfigDict(title = 'Сгенерированые access_token и refresh_token')
    
    
    
class IssuedJWTTokensWithDataOut(BaseModel):
    
    tokens : IssuedJWTTokensOut
    data : tuple[IssuedJWTTokenData, IssuedJWTTokenData] 
    
    
    

    