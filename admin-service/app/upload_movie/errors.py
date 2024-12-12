from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status
from core.exception import BaseHTTPException, BaseHTTPExceptionModel



class MovieUploadErrorType(StrEnum):
    INCORRECT_FILE_TYPE = auto()



class MovieUploadExceptionModel(BaseHTTPExceptionModel):
    
    type : MovieUploadErrorType
    
    model_config = ConfigDict(title = 'Ошибка при изменении файлов фильма')




class MovieUploadException(BaseHTTPException):
    pass



IncorrectFileTypeError = MovieUploadException(status_code = status.HTTP_400_BAD_REQUEST,
                                            ditail = MovieUploadExceptionModel(
                                                type = MovieUploadErrorType.INCORRECT_FILE_TYPE,
                                                message = 'content-type shoud be video/mp4'
                                            )
                                        )
