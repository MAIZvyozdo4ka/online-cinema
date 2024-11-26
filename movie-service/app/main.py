from fastapi import FastAPI
from core.exeption import BaseHTTPExeption, http_exeption_handler
from .action import action_router
from .search import search_router


app = FastAPI(  
        root_path = '/api/v1',
        exception_handlers = {
        BaseHTTPExeption : http_exeption_handler
    }
)

app.include_router(search_router)
app.include_router(action_router)