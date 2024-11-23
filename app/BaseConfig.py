
from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import abspath, dirname


class BaseConfig(BaseSettings):
    SECRET : str
    model_config = SettingsConfigDict(
        extra = 'ignore',
        env_file = dirname(dirname(abspath(__file__))) + '/.env',
        frozen = True
    )
    