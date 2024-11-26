from fastapi import FastAPI
from core.exeption import BaseHTTPExeption, http_exeption_handler
from .rate import rate_action_couter
from .movie import movie_rating_router


app = FastAPI(  
        root_path = '/api/v1/rating',
        exception_handlers = {
        BaseHTTPExeption : http_exeption_handler
    }
)

app.include_router(rate_action_couter)
app.include_router(movie_rating_router)