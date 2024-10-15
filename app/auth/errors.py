from BaseHTTPExeption import BaseHTTPExeption, BaseHTTPExeptionModel
from pydantic import Field, ConfigDict
from enum import StrEnum
from fastapi import status





class AuthErrorType(StrEnum):
    EMAIL_OCCUPIED = 'email_occupied'
    USERNAME_OCCUPIED = 'username_occupied'
    INVALID_USERNAME_OR_EMAIL = 'invalid_username_or_email'
    INVALID_PASSWORD = 'invalid_password'
    USERNAME_LIKE_EMAIL = 'username_like_email'





class AuthExeptionModel(BaseHTTPExeptionModel):
    
    type : AuthErrorType = Field(description = 'Тип ошибки')
    message : str = Field(description = 'Подробности')
    
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


IncorrectUsernameError = AuthExeption(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = AuthExeptionModel(
                                                                    type = AuthErrorType.USERNAME_LIKE_EMAIL,
                                                                    message = 'This username is incorrect'
                                                                )
                                         )
