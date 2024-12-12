from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.exception import BaseHTTPException, http_Exception_handler
from .review import review_action_user
from .movie import movie_review_router


app = FastAPI(  
        root_path = '/api/v1/review',
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

app.include_router(review_action_user)
app.include_router(movie_review_router)