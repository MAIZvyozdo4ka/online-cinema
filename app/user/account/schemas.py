from app.BaseModel import BaseModel
from pydantic import ConfigDict, PositiveInt, computed_field
from app.user.movie_action.schemas import RateMovie, ReviewMovie, ShowUserActionMoiveOut




class ShowUserMovieRatingOut(RateMovie, ShowUserActionMoiveOut):

    model_config = ConfigDict(title = 'Иформация о фильме с оценкой от пользователя')
    


class ShowUserMovieReviewsOut(ShowUserActionMoiveOut, ReviewMovie):
    
    model_config = ConfigDict(title = 'Иформация о фильме с отзывом от пользователя')
    
   
   
    
class ShowUserMovieReviewsListOut(BaseModel):
    reviews_list : list[ShowUserMovieReviewsOut] 
    
    model_config = ConfigDict(title = 'Иформация об отзывах фильмов оставленных пользователем')
    
    @computed_field(description = 'Количество отзывов оставленных пользователем')
    @property
    def reviews_count(self) -> PositiveInt:
        return len(self.reviews_list) 


  
  
class ShowUserMovieRatingListOut(BaseModel):
    rate_list : list[ShowUserMovieRatingOut] 
    
    model_config = ConfigDict(title = 'Иформация об оценках фильмов оставленных пользователем')
    
    @computed_field(description = 'Количество оценок оставленных пользователем')
    @property
    def rating_count(self) -> PositiveInt:
        return len(self.rate_list)
    