from app.BaseHTTPException import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import Field, ConfigDict
from fastapi import status


class MovieExceptionModel(BaseHTTPExceptionModel):
    
    model_config = ConfigDict(title = 'Ошибка, связанная с фильмом')
    
    
    
class MovieHTTPException(BaseHTTPException):
    pass
        
        

MovieNotFoundError = MovieHTTPException(status.HTTP_404_NOT_FOUND, MovieExceptionModel(message = 'no movie with this id'))
