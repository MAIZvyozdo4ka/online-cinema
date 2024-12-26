from pydantic import Field, ConfigDict, computed_field
from core.schemas import BaseModel, MovieModelOut



class TextSearchIn(BaseModel):
    
    text : str | None = Field(default = None, description = 'Поисковой запрос', min_length = 1, max_length = 50)
    
    model_config = ConfigDict(title = 'Запрос фильмов')

    
    
    
    
class MoviePreviewOut(MovieModelOut):
    
    model_config = ConfigDict(title = 'Краткая информация о фильме')
    
    
    
    
    
    
    
