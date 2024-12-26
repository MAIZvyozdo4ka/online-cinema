from core.schemas import BaseModel, MovieID, ReviewMovieWithUserInfoOut
from pydantic import Field, ConfigDict, PositiveInt

class DeleteReviewIn(BaseModel):
    movie_id : MovieID = Field(description = 'ID фильма')
    user_id : PositiveInt = Field(description = 'ID пользователя')
    
    model_config = ConfigDict(title = 'Форма для удаления рецензии')
    
    
    
class ReviewMovieWithUserInfoAndMovieIDOut(ReviewMovieWithUserInfoOut):
    movie_id : MovieID = Field(description = 'ID фильма')
    
    model_config = ConfigDict(title = 'Рецензия фильма')