from BaseHTTPExeption import BaseHTTPExeption, BaseHTTPExeptionModel
from pydantic import Field, ConfigDict
from fastapi import status


class SearchExeptionModel(BaseHTTPExeptionModel):
    msg : str = Field(description = 'message')
    
    model_config = ConfigDict(title = 'Ошибка при поиске')
    
    
    
class SearchHTTPExeption(BaseHTTPExeption):
    pass
        
        

SearchEmptyError = SearchHTTPExeption(status.HTTP_404_NOT_FOUND, SearchExeptionModel(msg = 'no movies'))

    

    
    
    