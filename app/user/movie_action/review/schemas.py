from pydantic import ConfigDict
from app.user.movie_action.schemas import ReviewMovie, ModelWithPrivateUserIdAndMovieId, BaseDeletedModel, UserActionOut

    
    
class ReviewMovieIn(ReviewMovie, ModelWithPrivateUserIdAndMovieId):
    model_config = ConfigDict(title = 'Форма для отправки рецензии')
    
 

class DeleteReviewMovieIn(BaseDeletedModel):
    
    model_config = ConfigDict(title = 'Форма для удаления рецензии')
    
    
    
    
class ReviewMovieOut(UserActionOut):
    pass



