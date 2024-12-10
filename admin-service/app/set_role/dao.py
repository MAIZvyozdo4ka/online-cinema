from .schemas import UserNewRoleIn
from core.models.postgres import UserDB, UserRole
from core.dao import PostgresDAO, AsyncSession
from core.dependencies.JWTToken import JWTTokenDAO
from sqlalchemy import update
from .errors import UserHaveRoleError, UserNotFoundError, IsAdminError



class SetRoleDAO(PostgresDAO):
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def set_moderator_role(cls, session : AsyncSession, user_role : UserNewRoleIn) -> None:
        user = await session.get(UserDB, user_role.user_id)
        
        if user is None:
            raise UserNotFoundError
        
        if user.role == UserRole.admin:
            raise IsAdminError
        
        if user.role == user_role.role:
            raise UserHaveRoleError
        
        
        query_for_change_role = update(UserDB).where(UserDB.id == user_role.user_id).values(role = user_role.role)
        await session.execute(query_for_change_role)
        await JWTTokenDAO.delete_all_user_tokens_by_user_id(session, user.id)
        