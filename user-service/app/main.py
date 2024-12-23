from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.exception import BaseHTTPException, http_Exception_handler
from .account import account_router
from .recommendation import rec_router

app = FastAPI(
        root_path = '/api/v1/me',
        exception_handlers = {
        BaseHTTPException : http_Exception_handler
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешаем запросы с фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(account_router)
app.include_router(rec_router)