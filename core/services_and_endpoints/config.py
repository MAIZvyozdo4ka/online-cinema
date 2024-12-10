from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import abspath, dirname, join


class ServicesURLsSettings(BaseSettings):
    AUTH_SERVICE : str
    S3 : str
    model_config = SettingsConfigDict(
        extra = 'ignore',
        env_file = dirname(dirname(abspath(__file__))) + '/env/services.env',
        frozen = True
    )
    
    
class EndpointsSettings(BaseSettings):
    LOGIN_ENDPOINT : str
    REGISTRATION_ENDPOINT : str
    MOVIE_ENDPOINT : str
    
    model_config = SettingsConfigDict(
        extra = 'ignore',
        env_file = dirname(dirname(abspath(__file__))) + '/env/endpoints.env',
        frozen = True
    )
    
    

servicesurls = ServicesURLsSettings()

endpoints = EndpointsSettings()
