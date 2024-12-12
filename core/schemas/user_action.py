from pydantic import Field, ConfigDict, field_serializer, PositiveInt, computed_field, PrivateAttr
from .BaseModel import BaseModel
from enum import StrEnum, auto
from .movie import MovieModelOut, MovieID
from datetime import datetime



class SuccessUserActionStatusType(StrEnum):
    SUCCESS_INSERT = auto()
    SUCCESS_UPDATE = auto()
    SUCCESS_DELETE = auto()
    


class UserActionOut(BaseModel):
    
    status : SuccessUserActionStatusType = Field(description = 'Статус изменения')
    
    model_config = ConfigDict(title = 'Успешное завершение изменения')
    
 
 
class ModelWithPrivateUserIdAndMovieId(BaseModel):
    _user_id : int = PrivateAttr()
    movie_id : MovieID = Field(description = 'ID фильма')
    
    @computed_field(alias = 'user_id')
    @property
    def user_id(self) -> int:
        return self._user_id
   
    
    
class BaseDeletedModel(ModelWithPrivateUserIdAndMovieId):
    pass



class UserActionMovie(BaseModel):
    last_modified : datetime = Field(description = 'Последняя дата изменения', validation_alias = 'updated_at')

    @field_serializer('last_modified')
    @classmethod
    def serialize_last_modified(cls, last_modified: datetime) -> str:
        return last_modified.strftime('%d-%m-%Y %H:%M:%S')



class ShowUserActionMoiveOut(UserActionMovie):
    movie : MovieModelOut 