from fastapi import FastAPI
from core.exeption import BaseHTTPExeption, http_exeption_handler
from .account import account_router

app = FastAPI(  
        root_path = '/api/v1/me',
        exception_handlers = {
        BaseHTTPExeption : http_exeption_handler
    }
)

app.include_router(account_router)