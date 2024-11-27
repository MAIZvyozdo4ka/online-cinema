from .rate import rate_action_couter
from .review import review_action_user
from fastapi import APIRouter


action_router = APIRouter(prefix = '/action')

action_router.include_router(review_action_user)
action_router.include_router(rate_action_couter)