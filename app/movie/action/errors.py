from app.BaseHTTPExeption import BaseHTTPExeption, BaseHTTPExeptionModel
from pydantic import Field, ConfigDict
from fastapi import status


class MovieExeptionModel(BaseHTTPExeptionModel):
    
    model_config = ConfigDict(title = 'Ошибка, связанная с фильмом')
    
    
    
class MovieHTTPExeption(BaseHTTPExeption):
    pass
        
        

MovieNotFoundError = MovieHTTPExeption(status.HTTP_404_NOT_FOUND, MovieExeptionModel(message = 'no movie with this id'))
