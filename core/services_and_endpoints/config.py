from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import abspath, dirname, join


class ServicesURLsSettings(BaseSettings):
    AUTH_SERVICE : str
    model_config = SettingsConfigDict(
        extra = 'ignore',
        env_file = dirname(abspath(__file__)) + '/services.env',
        frozen = True
    )
    
    
class EndpointsSettings(BaseSettings):
    LOGIN_ENDPOINT : str
    REGISTRATION_ENDPOINT : str
    
    model_config = SettingsConfigDict(
        extra = 'ignore',
        env_file = dirname(abspath(__file__)) + '/endpoints.env',
        frozen = True
    )
    
    

servicesurls = ServicesURLsSettings()

endpoints = EndpointsSettings()
