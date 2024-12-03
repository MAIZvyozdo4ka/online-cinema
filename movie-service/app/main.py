from fastapi import FastAPI
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

app.mount("/static", StaticFiles(directory="./app/static"), name="static")

app.include_router(search_router)
app.include_router(action_router)