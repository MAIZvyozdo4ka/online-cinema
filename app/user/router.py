from .account import user_account_router
from .movie_action import action_router
from fastapi import APIRouter, Depends
from app.JWTToken import JWTExeption, TokenValidation



router = APIRouter(prefix = '/user',
                        dependencies = [Depends(TokenValidation.check_access_token)],
                        responses = JWTExeption.get_responses_schemas()
                    )

router.include_router(user_account_router)
router.include_router(action_router)
