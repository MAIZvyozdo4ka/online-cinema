from app.BaseConfig import BaseConfig
from datetime import timedelta



class JWTTokenSettings(BaseConfig):
    SECRET : str
    ALGORITHM : str
    ACCESS_TOKEN_TTL : timedelta
    REFRESH_TOKEN_TTL : timedelta
    
    


jwtsettings = JWTTokenSettings()

