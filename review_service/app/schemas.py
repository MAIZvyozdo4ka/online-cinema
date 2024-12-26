from pydantic import Field, ConfigDict
from core.schemas import BaseModel
from core.models.postgres import StatementReviewType





class ReviewMovie(BaseModel):
    header : str = Field(min_length = 10, max_length = 100, description = 'Заголовок рецензии')
    review : str = Field(min_length = 10, description = 'Текстовое описание рецензии')
    statement : StatementReviewType = Field(description = 'Тип рецензии')
    
    model_config = ConfigDict(title = 'Pецензия')