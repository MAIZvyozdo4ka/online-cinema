from pydantic import Field, ConfigDict, field_serializer, PositiveInt, computed_field, PrivateAttr
from app.BaseModel import BaseModel
from enum import StrEnum, auto
from app.movie.schemas import MovieModelOut
from datetime import datetime
from app.database import StatementReviewType




class SuccessUserActionStatusType(StrEnum):
    SUCCESS_INSERT = auto()
    SUCCESS_UPDATE = auto()
    SUCCESS_DELETE = auto()
    


class UserActionOut(BaseModel):
    
    status : SuccessUserActionStatusType = Field(description = 'Статус изменения')
    
    model_config = ConfigDict(title = 'Успешное завершение изменения')
    
 
 
 
class RateMovie(BaseModel):
    rating : PositiveInt = Field(ge = 1, le = 10, description = 'Оценка фильма')
    
    model_config = ConfigDict(title = 'Оценка фильма')
       
    
    
    
class ReviewMovie(BaseModel):
    header : str = Field(min_length = 10, max_length = 100, description = 'Заголовок рецензии')
    review : str = Field(min_length = 10, description = 'Текстовое описание рецензии')
    statement : StatementReviewType = Field(description = 'Тип рецензии')
    
    model_config = ConfigDict(title = 'Pецензия')
    


class UserMoiveActionsInfo(BaseModel):
    user_movie_rate : RateMovie | None = Field(default = None)
    user_movie_review : ReviewMovie | None = Field(default = None)
    
    model_config = ConfigDict(title = 'Мнение пользователя о фильме')
    
    
    
    
class ModelWithPrivateUserIdAndMovieId(BaseModel):
    _user_id : int = PrivateAttr()
    movie_id : PositiveInt = Field(le = 10_000_000, description = 'ID фильма')
    
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