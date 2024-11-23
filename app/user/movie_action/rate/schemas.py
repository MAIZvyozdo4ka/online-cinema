from pydantic import ConfigDict
from app.user.movie_action.schemas import RateMovie, ModelWithPrivateUserIdAndMovieId, BaseDeletedModel, UserActionOut


class RateMovieIn(RateMovie, ModelWithPrivateUserIdAndMovieId):

    model_config = ConfigDict(title = 'Форма для отправки оценки фильма')
    
    
    
class DeleteRateMovieIn(BaseDeletedModel):
    
    model_config = ConfigDict(title = 'Форма для удаления оценки фильма')
    
    
    
class RateMovieOut(UserActionOut):
    pass
    
