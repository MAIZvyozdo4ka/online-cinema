from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.exeption import BaseHTTPExeption, http_exeption_handler
from .auth import auth_router

app = FastAPI(
    root_path='/api/v1/auth',
    exception_handlers={
        BaseHTTPExeption: http_exeption_handler
    }
)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Укажите фронтенд URL. Используйте ["*"] для всех источников.
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, OPTIONS и т. д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

# Подключаем маршруты
app.include_router(auth_router)
