from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from core.exception import BaseHTTPException, http_Exception_handler
from .action import action_router
from .search import search_router


app = FastAPI(  
        root_path = '/api/v1',
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

app.mount("/static", StaticFiles(directory="./app/static"), name="static")

app.include_router(search_router)
app.include_router(action_router)