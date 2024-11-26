from fastapi import FastAPI
from core.exeption import BaseHTTPExeption, http_exeption_handler
from .auth import auth_router


app = FastAPI(  
        root_path = '/api/v1/auth',
        exception_handlers = {
        BaseHTTPExeption : http_exeption_handler
    }
)

app.include_router(auth_router)