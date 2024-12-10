from fastapi import FastAPI
from core.exception import BaseHTTPException, http_Exception_handler
from .account import account_router

app = FastAPI(  
        root_path = '/api/v1/me',
        exception_handlers = {
        BaseHTTPException : http_Exception_handler
    }
)

app.include_router(account_router)