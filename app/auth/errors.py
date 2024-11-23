from app.BaseHTTPExeption import BaseHTTPExeption, BaseHTTPExeptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class AuthErrorType(StrEnum):
    EMAIL_OCCUPIED = auto()
    USERNAME_OCCUPIED = auto()
    INVALID_USERNAME_OR_EMAIL = auto()
    INVALID_PASSWORD = auto()





class AuthExeptionModel(BaseHTTPExeptionModel):
    
    type : AuthErrorType
 
    model_config = ConfigDict(title = 'Ошибка регистации')




class AuthExeption(BaseHTTPExeption):
    pass




EmailOccupiedError = AuthExeption(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = AuthExeptionModel(
                                                                    type = AuthErrorType.EMAIL_OCCUPIED,
                                                                    message = 'This email is already occupied'
                                                                )
                                         )

UsernameOccupiedError = AuthExeption(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = AuthExeptionModel(
                                                                    type = AuthErrorType.USERNAME_OCCUPIED,
                                                                    message = 'This username is already occupied'
                                                                )
                                         )


InvalidUsernameOrEmailError = AuthExeption(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = AuthExeptionModel(
                                                                    type = AuthErrorType.INVALID_USERNAME_OR_EMAIL,
                                                                    message = 'This username or email not registrate'
                                                                )
                                         )

InvalidPasswordError = AuthExeption(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = AuthExeptionModel(
                                                                    type = AuthErrorType.INVALID_PASSWORD,
                                                                    message = 'This password is inccorect'
                                                                )
                                         )


