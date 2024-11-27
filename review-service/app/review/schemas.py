from pydantic import ConfigDict, computed_field, PositiveInt
from core.schemas import ModelWithPrivateUserIdAndMovieId, BaseDeletedModel, UserActionOut, BaseModel, ShowUserActionMoiveOut
from ..schemas import ReviewMovie
    
    
    
class ReviewMovieIn(ReviewMovie, ModelWithPrivateUserIdAndMovieId):
    model_config = ConfigDict(title = 'Форма для отправки рецензии')
    
 

class DeleteReviewMovieIn(BaseDeletedModel):
    
    model_config = ConfigDict(title = 'Форма для удаления рецензии')
    
    
    
    
class ReviewMovieOut(UserActionOut):
    pass




class ShowUserMovieReviewsOut(ShowUserActionMoiveOut, ReviewMovie):
    
    model_config = ConfigDict(title = 'Иформация о фильме с отзывом от пользователя')
    
   
   
    
class ShowUserMovieReviewsListOut(BaseModel):
    reviews_list : list[ShowUserMovieReviewsOut] 
    
    model_config = ConfigDict(title = 'Иформация об отзывах фильмов оставленных пользователем')
    
    @computed_field(description = 'Количество отзывов оставленных пользователем')
    @property
    def reviews_count(self) -> PositiveInt:
        return len(self.reviews_list) 

