from app.BaseHTTPExeption import BaseHTTPExeption, BaseHTTPExeptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status


class RateErrorType(StrEnum):
    RATE_NOT_FOUND = auto()
    MOVIE_NOT_FOUND = auto()



class RatingExeptionModel(BaseHTTPExeptionModel):
    
    type : RateErrorType
    
    model_config = ConfigDict(title = 'Ошибка при оценке фильма')




class RatingExeption(BaseHTTPExeption):
    pass



RateNotFoundError = RatingExeption(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = RatingExeptionModel(
                                                                    type = RateErrorType.RATE_NOT_FOUND,
                                                                    message = 'the score was not found'
                                                                )
                                        )

MovieNotFoundError = RatingExeption(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = RatingExeptionModel(
                                                                    type = RateErrorType.MOVIE_NOT_FOUND,
                                                                    message = 'no movie with this id'
                                                                )
                                        )


