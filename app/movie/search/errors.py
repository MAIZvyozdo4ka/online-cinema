from app.BaseHTTPException import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import Field, ConfigDict
from fastapi import status


class SearchExceptionModel(BaseHTTPExceptionModel):
    
    model_config = ConfigDict(title = 'Ошибка при поиске')
    
    
    
class SearchHTTPException(BaseHTTPException):
    pass
        
        

SearchEmptyError = SearchHTTPException(status.HTTP_404_NOT_FOUND, SearchExceptionModel(message = 'no movies'))

    

    
    
    