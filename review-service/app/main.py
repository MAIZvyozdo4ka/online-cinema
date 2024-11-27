from fastapi import FastAPI
from core.exeption import BaseHTTPExeption, http_exeption_handler
from .review import review_action_user
from .movie import movie_review_router


app = FastAPI(  
        root_path = '/api/v1/review',
        exception_handlers = {
        BaseHTTPExeption : http_exeption_handler
    }
)

app.include_router(review_action_user)
app.include_router(movie_review_router)