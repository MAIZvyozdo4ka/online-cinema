import jwt
from datetime import datetime, timedelta
from .config import jwtsettings
from .JWTTokenType import JWTTokenType
from uuid import uuid4
from .schemas import IssuedJWTTokenData, IssuedJWTTokensWithDataOut, IssuedJWTTokensOut, NonPrivateUserInfoOut


class JWTToken:
    
    
    @classmethod
    def generate_access_token(cls, token_data : IssuedJWTTokenData) -> str:
        return cls.__sign_token(
            type = JWTTokenType.ACCESS,
            token_data = token_data,
            ttl = jwtsettings.ACCESS_TOKEN_TTL
        )
        
        
    
    @classmethod
    def generate_refresh_token(cls, token_data : IssuedJWTTokenData) -> str:
        return cls.__sign_token(
            type = JWTTokenType.REFRESH,
            token_data = token_data,
            ttl = jwtsettings.REFRESH_TOKEN_TTL
        )
      
        
    
    @staticmethod
    def verify_token(token : str) -> dict[str, str | int]:
        return jwt.decode(jwt = token, key = jwtsettings.SECRET, algorithms = [jwtsettings.ALGORITHM])



    @classmethod
    def get_jti(cls, token : str) -> str:
        return cls.verify_token(token)['jti']



    @classmethod
    def get_sub(cls, token : str) -> str:
        return cls.verify_token(token)['sub']



    @classmethod
    def get_exp(cls, token : str) -> int:
        return cls.verify_token(token)['exp']
    
    
    
    @classmethod
    def is_active_token(cls, token : str) -> bool:
        return (cls.get_exp(token) - cls.get_numeric_date_time_now()) > 0
    
    
    
    @staticmethod
    def get_numeric_date_time_now() -> int:
        return int(datetime.now().timestamp())
    
    
    
    @classmethod
    def __sign_token(cls, type: str, token_data : IssuedJWTTokenData, ttl : timedelta) -> str:
        numeric_date_time_now = cls.get_numeric_date_time_now()
        
        payload = {
            'iss' : 'zvezdochka@auth_service',
            'type' : type,
            'iat' : numeric_date_time_now,
            'exp' : numeric_date_time_now  + int(ttl.total_seconds())
        }
        payload = payload | token_data.model_dump()
        payload['jti'] = str(payload['jti'])
        print(payload)
        
        return jwt.encode(payload = payload, key = jwtsettings.SECRET, algorithm = jwtsettings.ALGORITHM)
    
    
    @staticmethod
    def generate_device_id() -> str:
        return str(uuid4())
    
    
    
    @classmethod
    def generate_tokens(cls, payload : NonPrivateUserInfoOut) -> IssuedJWTTokensWithDataOut:
        device_id = cls.generate_device_id()
        
        access_token_data, refresh_token_data = [IssuedJWTTokenData(device_id = device_id,
                                                                    **payload.model_dump()
                                                                ) for _ in range(2)
                                                            ]
        return IssuedJWTTokensWithDataOut(
                        tokens = IssuedJWTTokensOut(
                            access_token = JWTToken.generate_access_token(access_token_data),
                            refresh_token = JWTToken.generate_refresh_token(refresh_token_data)
                        ),
                        data = (access_token_data, refresh_token_data)
                    )
        
    
    
    
    
