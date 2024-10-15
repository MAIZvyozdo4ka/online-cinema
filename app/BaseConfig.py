import os
from pydantic_settings import BaseSettings, SettingsConfigDict



class BaseConfig(BaseSettings):
    
    model_config = SettingsConfigDict(
        extra = 'ignore',
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        frozen = True
    )