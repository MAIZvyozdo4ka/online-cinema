from pydantic import ConfigDict, PositiveInt, Field, computed_field
from ..schemas import RateMovie


    
class MovieRatingOut(RateMovie):
    rating_count : PositiveInt = Field(description = 'Количество оценок')
    
    model_config = ConfigDict(title = 'Статистика оценок фильма')