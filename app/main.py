from fastapi import FastAPI, Depends
from .movie import movie_router
from .JWTToken import TokenValidation
from .BaseHTTPException import http_Exception_handler, BaseHTTPException
from .auth import auth_router
from .user import user_router



app = FastAPI(  
        exception_handlers = {
        BaseHTTPException : http_Exception_handler
    }
)

app.include_router(movie_router)
app.include_router(auth_router)
app.include_router(user_router)



#print(BaseHTTPException._all_responses_schemas)