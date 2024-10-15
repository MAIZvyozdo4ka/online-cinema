from BaseHTTPExeption import BaseHTTPExeption, BaseHTTPExeptionModel
from pydantic import Field, ConfigDict
from enum import StrEnum
from fastapi import status




class AccessErrorType(StrEnum):
    TOKEN_IS_NOT_SPECIFIED = 'token_is_not_specified'
    INCORRECT_AUTH_HEADER_FORM = 'incorrect_auth_header_form'
    INCORRECT_TOKEN_TYPE = 'incorrect_token_type'
    INVALID_TOKEN = 'invalid_token'
    TOKEN_HAS_EXPIRED = 'token_has_expired'
    TOKEN_OWNER_NOT_FOUND = 'token_owner_not_found'
    TOKEN_REVOKED = 'token_revoked'


    
    
class JWTExeptionModel(BaseHTTPExeptionModel):
    
    type : AccessErrorType = Field(description = 'Тип ошибки')
    message : str = Field(description = 'Подробности')
    
    model_config = ConfigDict(title = 'Ошибка авторизации')



class JWTExeption(BaseHTTPExeption):
    pass



IsNotSpecifiedError = JWTExeption(status_code = status.HTTP_307_TEMPORARY_REDIRECT,
                                  ditail = JWTExeptionModel(
                                                            type = AccessErrorType.TOKEN_IS_NOT_SPECIFIED,
                                                            message = 'Access-token header is not set'
                                                        ),
                                  headers = {
                                        'Location' : '/auth/registration'
                                    }
                                  )

IncorrectAuthHeaderFromError = JWTExeption(status_code = status.HTTP_401_UNAUTHORIZED,
                                         ditail = JWTExeptionModel(
                                                            type = AccessErrorType.INCORRECT_AUTH_HEADER_FORM,
                                                            message = 'Access-token must have the form "Bearer <TOKEN>"'
                                                        )
                                         )


IncorrectTokenTypeError = JWTExeption(status_code = status.HTTP_401_UNAUTHORIZED,
                                         ditail = JWTExeptionModel(
                                                                    type = AccessErrorType.INCORRECT_TOKEN_TYPE,
                                                                    message = 'The passed token does not match the required type'
                                                                )
                                         )

ClientInvalidTokenError = JWTExeption(status_code = status.HTTP_401_UNAUTHORIZED,
                                         ditail = JWTExeptionModel(
                                                                    type = AccessErrorType.INVALID_TOKEN,
                                                                    message = 'The transferred token is invalid'
                                                                )
                                         )


ExpiredTokenError = JWTExeption(status_code = status.HTTP_401_UNAUTHORIZED,
                                         ditail = JWTExeptionModel(
                                                                    type = AccessErrorType.TOKEN_HAS_EXPIRED,
                                                                    message = 'The token lifetime has expired'
                                                                )
                                         )

TokenRevokedError = JWTExeption(status_code = status.HTTP_401_UNAUTHORIZED,
                                         ditail = JWTExeptionModel(
                                                                    type = AccessErrorType.TOKEN_REVOKED,
                                                                    message = 'This token has revoked'
                                                                )
                                         )