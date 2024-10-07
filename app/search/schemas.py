from pydantic import BaseModel, Field, ConfigDict, field_serializer, field_validator



class TextSearchRequest(BaseModel):
    
    text : str | None = Field(default = None, description = 'Поисковой запрос', min_length = 1, max_length = 50)
    
    
    model_config = ConfigDict(title = 'Запрос фильмов', frozen = True)
   
   
   
class LinkResponse(BaseModel):
    
    imdb_link : int | None = Field(default = None, validation_alias = 'imdb_id', description = 'Ссылка на IMDB')
    tmbd_link : int | None = Field(default = None, validation_alias = 'tmbd_id', description = 'Ссылка на TMDB')
    
    
    model_config = ConfigDict(title = 'Cсылки на другие сайты',frozen = True, from_attributes = True, extra = 'ignore')
    
    
    @field_serializer('imdb_link')
    def serializer_imdb_link(self, imdb_link : int | None) -> str:
        if imdb_link is None:
            return ''
        zeros_count : int = 7 - len(str(imdb_link))
        return f'https://www.imdb.com/title/tt{"0" * zeros_count}{imdb_link}'
    
    
    @field_serializer('tmbd_link')
    def serializer_tmdb_link(self, tmbd_link : int | None) -> str:
        if tmbd_link is None:
            return ''
        return f'https://www.themoviedb.org/movie/{tmbd_link}'
    
    
    
class MovieResponse(BaseModel):
    
    title : str = Field(description = 'Назавние фильма')
    genres : str = Field(description = 'Жанры фильма')
    links : LinkResponse = Field(description = 'Ссылки на фильм', validation_alias = 'link')
    
    
    model_config = ConfigDict(title = 'Информация о фильме', frozen = True, from_attributes = True, extra = 'ignore')
    
    
    @field_serializer('genres')
    def serializer_genres(self, genres : str) -> list[str]:
        return genres.split('|')
    
    
    @field_validator('links', mode = 'before')
    @classmethod
    def validate_links(cls, links : list[LinkResponse]) -> LinkResponse:
        return links[0]
    
    
