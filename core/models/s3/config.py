from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import abspath, dirname


CONFIG_FILE = dirname(dirname(dirname(abspath(__file__)))) + '/env/s3_config.env'


class S3Config(BaseSettings):
    MOVIE_BUCKET_NAME : str
    MOVIE_BUCKET_ACL : str
    REGION : str
    model_config = SettingsConfigDict(
        extra = 'ignore',
        env_file = CONFIG_FILE,
        frozen = True
    )


s3config = S3Config()