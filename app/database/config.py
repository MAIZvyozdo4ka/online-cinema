from BaseConfig import BaseConfig


class DBSettings(BaseConfig):
    DB_HOST : str
    DB_PORT : int
    DB_NAME : str
    DB_USER : str
    DB_PASSWORD : str
    
    
    
settings = DBSettings()


def get_db_url() -> str:
    return (f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@'
            f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')
    
