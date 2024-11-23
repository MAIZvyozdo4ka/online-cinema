from pydantic import Field, ConfigDict, field_serializer, computed_field
from app.BaseModel import BaseModel
   




class MovieModelOut(BaseModel):
    
    id : int = Field(exclude = True)
    title : str = Field(description = 'Назавние фильма')
    genres : str = Field(description = 'Жанры фильма')
    rating : float = Field(description = 'Средняя оценка фильма', validation_alias = 'movie_rating_avg')
    rating_count : int = Field(description = 'Количество оценок фильма', validation_alias = 'movie_rating_count')
    review_count : int = Field(description = 'Количество рецензий фильма', validation_alias = 'movie_reviews_count')
    
    model_config = ConfigDict(title = 'Информация о фильме')
    
    @field_serializer('genres')
    @classmethod
    def serializer_genres(cls, genres : str) -> list[str]:
        return genres.split('|')
    
    @computed_field(description = 'Ссылка для открытия фильма')
    @property
    def local_link(self) -> str:
        zeros_count : int = 7 - len(str(self.id))
        
        return f'movie/{"0" * zeros_count}{self.id}'
    
    