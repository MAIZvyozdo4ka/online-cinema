from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status
from app.BaseHTTPExeption import BaseHTTPExeption, BaseHTTPExeptionModel



class ReviewErrorType(StrEnum):
    MOVIE_NOT_FOUND = auto()
    REVIEW_NOT_FOUND = auto()




class ReviewExeptionModel(BaseHTTPExeptionModel):
    
    type : ReviewErrorType
    
    model_config = ConfigDict(title = 'Ошибка при написанни отзыва')




class ReviewExeption(BaseHTTPExeption):
    pass




ReviewNotFoundError = ReviewExeption(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = ReviewExeptionModel(
                                                                    type = ReviewErrorType.REVIEW_NOT_FOUND,
                                                                    message = 'the score was not found'
                                                                )
                                        )

MovieNotFoundError = ReviewExeption(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = ReviewExeptionModel(
                                                                    type = ReviewErrorType.MOVIE_NOT_FOUND,
                                                                    message = 'no movie with this id'
                                                                )
                                        )
