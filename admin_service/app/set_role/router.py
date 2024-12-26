from fastapi import APIRouter, Request, Depends, Path
from .schemas import UserNewRoleIn
from .dao import SetRoleDAO
from core.schemas import UserActionOut, SuccessUserActionStatusType
from .errors import SetRoleException



router = APIRouter(
                    tags = ['Изменение ролей'], 
                    responses = SetRoleException.get_responses_schemas()
                )



@router.post('/set-role', summary = 'Выдать роль')
async def create_new_moive(user_role : UserNewRoleIn) -> UserActionOut:
    await SetRoleDAO.set_moderator_role(user_role)
    return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_UPDATE)
 

