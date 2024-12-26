from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status
from core.exception import BaseHTTPException, BaseHTTPExceptionModel



class ModeratorReviewErrorType(StrEnum):
    REVIEW_NOT_FOUND = auto()



class ModeratorReviewExceptionModel(BaseHTTPExceptionModel):
    
    type : ModeratorReviewErrorType
    
    model_config = ConfigDict(title = 'Ошибка при изменении модератором рецензий')




class ModeratorReviewException(BaseHTTPException):
    pass



ReviewNotFoundError = ModeratorReviewException(status_code = status.HTTP_400_BAD_REQUEST,
                                               ditail = ModeratorReviewExceptionModel(
                                                   type = ModeratorReviewErrorType.REVIEW_NOT_FOUND,
                                                   message = 'review not found'
                                               )
                                            )

