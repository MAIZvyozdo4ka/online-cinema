from fastapi import FastAPI, Depends
from .movie import movie_router
from .JWTToken import TokenValidation
from .BaseHTTPExeption import http_exeption_handler, BaseHTTPExeption
from .auth import auth_router
from .user import user_router



app = FastAPI(  
        exception_handlers = {
        BaseHTTPExeption : http_exeption_handler
    }
)

app.include_router(movie_router)
app.include_router(auth_router)
app.include_router(user_router)



#print(BaseHTTPExeption._all_responses_schemas)
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешаем запросы с фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)"""