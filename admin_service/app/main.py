from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from core.exception import BaseHTTPException, http_exception_handler
from .moive import admin_moive_action_router
from .set_role import set_role_router
from .upload_movie import upload_movie_router
from core.dependencies.Role import RoleValidation, RoleException
from core.models.postgres import UserRole



app = FastAPI(  
        root_path = '/api/v1/admin',
        dependencies = [Depends(RoleValidation.check_role_right(UserRole.admin))],
        responses = RoleException.get_responses_schemas(),
        exception_handlers = {
        BaseHTTPException : http_exception_handler
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

app.include_router(admin_moive_action_router)
app.include_router(set_role_router)
app.include_router(upload_movie_router)
