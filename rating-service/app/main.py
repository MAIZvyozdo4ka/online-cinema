from fastapi import FastAPI
from core.exception import BaseHTTPException, http_Exception_handler
from .rate import rate_action_couter
from .movie import movie_rating_router


app = FastAPI(  
        root_path = '/api/v1/rating',
        exception_handlers = {
        BaseHTTPException : http_Exception_handler
    }
)

app.include_router(rate_action_couter)
app.include_router(movie_rating_router)