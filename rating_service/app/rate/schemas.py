from pydantic import ConfigDict, PositiveInt, Field, computed_field
from core.schemas import ModelWithPrivateUserIdAndMovieId, BaseDeletedModel, UserActionOut, ShowUserActionMoiveOut, BaseModel
from ..schemas import RateMovie




class RateMovieIn(RateMovie, ModelWithPrivateUserIdAndMovieId):

    model_config = ConfigDict(title = 'Форма для отправки оценки фильма')
    
    
    
class DeleteRateMovieIn(BaseDeletedModel):
    
    model_config = ConfigDict(title = 'Форма для удаления оценки фильма')
    
    
    
class RateMovieOut(UserActionOut):
    pass
    

class ShowUserMovieRatingOut(RateMovie, ShowUserActionMoiveOut):

    model_config = ConfigDict(title = 'Иформация о фильме с оценкой от пользователя')



class ShowUserMovieRatingListOut(BaseModel):
    rate_list : list[ShowUserMovieRatingOut] 
    
    model_config = ConfigDict(title = 'Иформация об оценках фильмов оставленных пользователем')
    
    @computed_field(description = 'Количество оценок оставленных пользователем')
    @property
    def rating_count(self) -> PositiveInt:
        return len(self.rate_list)