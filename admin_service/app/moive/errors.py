from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status
from core.exception import BaseHTTPException, BaseHTTPExceptionModel



class MovieActionErrorType(StrEnum):
    MOVIE_ALREADY_EXIST = auto()
    LINK_ALREADY_EXIST = auto()
    MOVIE_NOT_FOUND = auto()
    EMPTY_REQUEST = auto()



class MovieActionExceptionModel(BaseHTTPExceptionModel):
    
    type : MovieActionErrorType
    
    model_config = ConfigDict(title = 'Ошибка при изменении фильма')




class MovieActionException(BaseHTTPException):
    pass


MovieAlreadyExistError = MovieActionException(status_code = status.HTTP_400_BAD_REQUEST,
                                            ditail = MovieActionExceptionModel(
                                                type = MovieActionErrorType.MOVIE_ALREADY_EXIST,
                                                message = 'The film name already exists'
                                            )
                                        )

LinksAlreadyExistError = MovieActionException(status_code = status.HTTP_400_BAD_REQUEST,
                                            ditail = MovieActionExceptionModel(
                                                type = MovieActionErrorType.LINK_ALREADY_EXIST,
                                                message = 'The link already exists'
                                            )
                                        )

MovieNoFoundError = MovieActionException(status_code = status.HTTP_400_BAD_REQUEST,
                                            ditail = MovieActionExceptionModel(
                                                type = MovieActionErrorType.MOVIE_NOT_FOUND,
                                                message = 'No moive with this id'
                                            )
                                        )

EmptyRequestError = MovieActionException(status_code = status.HTTP_400_BAD_REQUEST,
                                            ditail = MovieActionExceptionModel(
                                                type = MovieActionErrorType.EMPTY_REQUEST,
                                                message = 'request body has no attribute'
                                            )
                                        )
