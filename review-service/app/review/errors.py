from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status
from core.exception import BaseHTTPException, BaseHTTPExceptionModel



class ReviewErrorType(StrEnum):
    MOVIE_NOT_FOUND = auto()
    REVIEW_NOT_FOUND = auto()




class ReviewExceptionModel(BaseHTTPExceptionModel):
    
    type : ReviewErrorType
    
    model_config = ConfigDict(title = 'Ошибка при написанни отзыва')




class ReviewException(BaseHTTPException):
    pass




ReviewNotFoundError = ReviewException(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = ReviewExceptionModel(
                                                                    type = ReviewErrorType.REVIEW_NOT_FOUND,
                                                                    message = 'the score was not found'
                                                                )
                                        )

MovieNotFoundError = ReviewException(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = ReviewExceptionModel(
                                                                    type = ReviewErrorType.MOVIE_NOT_FOUND,
                                                                    message = 'no movie with this id'
                                                                )
                                        )
