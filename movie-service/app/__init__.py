from .action import action_router
from .search import search_router
from fastapi import APIRouter


movie_router = APIRouter()

movie_router.include_router(action_router)
movie_router.include_router(search_router)