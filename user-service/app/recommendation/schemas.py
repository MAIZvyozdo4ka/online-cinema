from pydantic import Field, ConfigDict, computed_field
from core.schemas import BaseModel, MovieModelOut

    
class MoviePreviewOut(MovieModelOut):
    
    model_config = ConfigDict(title = 'Краткая информация о фильме')
    
    
    
    
    
    
    
