from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.exeption import BaseHTTPExeption, http_exeption_handler
from .rate import rate_action_couter
from .movie import movie_rating_router


app = FastAPI(  
        root_path = '/api/v1/rating',
        exception_handlers = {
        BaseHTTPExeption : http_exeption_handler
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешаем запросы с фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(rate_action_couter)
app.include_router(movie_rating_router)