from pydantic import Field, ConfigDict
from core.schemas import UserActionMovie, BaseModel, NonPrivateUserInfoOut
from ..schemas import ReviewMovie

    
 
class ReviewMovieWithUserInfoOut(UserActionMovie, ReviewMovie):
    user : NonPrivateUserInfoOut
    
    model_config = ConfigDict(title = 'Рецензии фильма')
    
    

class ReviewMovieWithUserInfoListWithStatisticOut(BaseModel):
    reviews : list[ReviewMovieWithUserInfoOut] = Field(description = 'Последние рецензии')
    reviews_count : int = Field(description = 'Количество рецензий фильма')
    positive_statement_percent : float = Field(description = 'Процент положительных рецензий фильма')
    negative_statement_percent : float = Field(description = 'Процент негативных рецензий фильма')
    neutral_statement_percent : float = Field(description = 'Процент нейтральных рецензий фильма')
    
    model_config = ConfigDict(title = 'Рецензии фильма со статистикой')
    
    
