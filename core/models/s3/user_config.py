from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import abspath, dirname
import json
from typing import Any

USERS_FILE_NAME = dirname(dirname(dirname(abspath(__file__)))) + '/env/s3_clients.json'


class S3SettingsKeys(BaseSettings):
    access : str
    secret : str


class S3UserSettings(BaseSettings):
    name : str
    keys : list[S3SettingsKeys]
    
    
    model_config = SettingsConfigDict(
        extra = 'ignore',
        frozen = True
    )


def any_user_to_dict(user_count : int) -> dict[str, Any]:
    with open(USERS_FILE_NAME, 'r') as file:
       return json.load(file)['accounts'][user_count]
    

admin_s3 = S3UserSettings.model_validate(any_user_to_dict(0))
user_s3 = S3UserSettings.model_validate(any_user_to_dict(1))