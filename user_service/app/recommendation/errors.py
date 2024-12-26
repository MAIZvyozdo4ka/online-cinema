from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import Field, ConfigDict
from fastapi import status


class RecExceptionModel(BaseHTTPExceptionModel):
    
    model_config = ConfigDict(title = 'Ошибка при поиске')
    
    
    
class RecHTTPException(BaseHTTPException):
    pass
        
        

RecEmptyError = RecHTTPException(status.HTTP_404_NOT_FOUND, RecExceptionModel(message = 'no movies'))

    

    
    
    