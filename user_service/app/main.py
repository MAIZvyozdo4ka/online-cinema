from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.exception import BaseHTTPException, http_exception_handler
from .account import account_router
from .recommendation import rec_router

app = FastAPI(
        root_path = '/api/v1/me',
        exception_handlers = {
        BaseHTTPException : http_exception_handler
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


app.include_router(account_router)
app.include_router(rec_router)