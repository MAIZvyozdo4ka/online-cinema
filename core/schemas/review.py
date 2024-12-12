from pydantic import Field, ConfigDict
from core.models.postgres import StatementReviewType
from .user_action import UserActionMovie
from .user import NonPrivateUserInfoOut
from .BaseModel import BaseModel
from .movie import MovieID


MAX_REVIEW_COUNT : int = 250



class ReviewMovie(BaseModel):
    header : str = Field(min_length = 10, max_length = 100, description = 'Заголовок рецензии')
    review : str = Field(min_length = 10, description = 'Текстовое описание рецензии')
    statement : StatementReviewType = Field(description = 'Тип рецензии')
    
    model_config = ConfigDict(title = 'Pецензия')
  
    
    
class ReviewMovieWithUserInfoOut(UserActionMovie, ReviewMovie):
    user : NonPrivateUserInfoOut
    
    model_config = ConfigDict(title = 'Рецензия фильма')
    

class ReviewMovieWithUserInfoAndMovieIDOut(ReviewMovieWithUserInfoOut):
    movie_id : MovieID = Field(description = 'ID фильма')
    
    model_config = ConfigDict(title = 'Рецензия фильма')