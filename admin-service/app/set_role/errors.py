from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status
from core.exception import BaseHTTPException, BaseHTTPExceptionModel



class SetRoleErrorType(StrEnum):
    USER_NOT_FOUND = auto()
    USER_HAVE_ROLE = auto()
    IS_ADMIN = auto()


class SetRoleExceptionModel(BaseHTTPExceptionModel):
    
    type : SetRoleErrorType
    
    model_config = ConfigDict(title = 'Ошибка при изменении роли пользователя')




class SetRoleException(BaseHTTPException):
    pass


UserNotFoundError = SetRoleException(status_code = status.HTTP_400_BAD_REQUEST,
                                     ditail = SetRoleExceptionModel(
                                        type = SetRoleErrorType.USER_NOT_FOUND,
                                        message = 'user not found'
                                     ) 
                                )

UserHaveRoleError = SetRoleException(status_code = status.HTTP_400_BAD_REQUEST,
                                     ditail = SetRoleExceptionModel(
                                        type = SetRoleErrorType.USER_HAVE_ROLE,
                                        message = 'role is set'
                                    ) 
                                )


IsAdminError = SetRoleException(status_code = status.HTTP_400_BAD_REQUEST,
                                     ditail = SetRoleExceptionModel(
                                        type = SetRoleErrorType.IS_ADMIN,
                                        message = 'role cant change for admin'
                                    ) 
                                )
