from fastapi import FastAPI, Depends
from core.exception import BaseHTTPException, http_Exception_handler
from core.dependencies.Role import RoleValidation, RoleException
from core.models.postgres import UserRole
from .reviews import moderator_review_router


app = FastAPI(  
        root_path = '/api/v1/moderator',
        dependencies = [Depends(RoleValidation.check_role_right(UserRole.moderator))],
        responses = RoleException.get_responses_schemas(),
        exception_handlers = {
        BaseHTTPException : http_Exception_handler
    }
)


app.include_router(moderator_review_router)