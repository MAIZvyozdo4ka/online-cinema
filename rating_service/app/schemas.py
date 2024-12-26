from pydantic import ConfigDict, PositiveInt, Field
from core.schemas import BaseModel




class RateMovie(BaseModel):
    rating : PositiveInt = Field(ge = 1, le = 10, description = 'Оценка фильма')
    
    model_config = ConfigDict(title = 'Оценка фильма')
