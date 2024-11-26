
from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import abspath, dirname


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra = 'ignore',
        env_file = dirname(dirname(abspath(__file__))) + '/.env',
        frozen = True
    )
    