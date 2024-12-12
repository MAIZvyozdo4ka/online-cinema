from core.schemas import BaseModel
from pydantic import Field, PositiveInt, field_serializer, ConfigDict
from core.models.postgres import UserRole



class UserNewRoleIn(BaseModel):
    user_id : PositiveInt = Field(description = 'ID пользователя')
    role : UserRole = Field(description = 'Новая роль', default = UserRole.user)
    
    model_config = ConfigDict(title = 'Выдача новой роли пользователю')