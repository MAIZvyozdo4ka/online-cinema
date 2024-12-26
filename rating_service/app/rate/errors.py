from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status


class RateErrorType(StrEnum):
    RATE_NOT_FOUND = auto()
    MOVIE_NOT_FOUND = auto()



class RatingExceptionModel(BaseHTTPExceptionModel):
    
    type : RateErrorType
    
    model_config = ConfigDict(title = 'Ошибка при оценке фильма')




class RatingException(BaseHTTPException):
    pass



RateNotFoundError = RatingException(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = RatingExceptionModel(
                                                                    type = RateErrorType.RATE_NOT_FOUND,
                                                                    message = 'the score was not found'
                                                                )
                                        )

MovieNotFoundError = RatingException(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = RatingExceptionModel(
                                                                    type = RateErrorType.MOVIE_NOT_FOUND,
                                                                    message = 'no movie with this id'
                                                                )
                                        )


