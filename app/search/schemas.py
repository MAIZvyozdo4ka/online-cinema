from pydantic import Field, ConfigDict, field_serializer, field_validator
from BaseSchema import Model



class TextSearchIn(Model):
    
    text : str | None = Field(default = None, description = 'Поисковой запрос', min_length = 1, max_length = 50)
    
    
    model_config = ConfigDict(title = 'Запрос фильмов')
   
   
   
class LinksForAnotherOut(Model):
    
    imdb_link : int | None = Field(default = None, validation_alias = 'imdb_id', description = 'Ссылка на IMDB')
    tmbd_link : int | None = Field(default = None, validation_alias = 'tmbd_id', description = 'Ссылка на TMDB')
    
    
    model_config = ConfigDict(title = 'Cсылки на другие сайты')
    
    
    @field_serializer('imdb_link')
    @classmethod
    def serializer_imdb_link(cls, imdb_link : int | None) -> str:
        if imdb_link is None:
            return ''
        zeros_count : int = 7 - len(str(imdb_link))
        return f'https://www.imdb.com/title/tt{"0" * zeros_count}{imdb_link}'
    
    
    @field_serializer('tmbd_link')
    @classmethod
    def serializer_tmdb_link(cls, tmbd_link : int | None) -> str:
        if tmbd_link is None:
            return ''
        return f'https://www.themoviedb.org/movie/{tmbd_link}'
  

    
    
    
class MoviePreviewOut(Model):
    
    title : str = Field(description = 'Назавние фильма')
    genres : str = Field(description = 'Жанры фильма')
    links : LinksForAnotherOut = Field(description = 'Ссылки на фильм', validation_alias = 'link')
    local_link : int = Field(validation_alias = 'movie_id', description = 'Ссылка для открытия фильма')
    
    model_config = ConfigDict(title = 'Информация о фильме')
    
    
    @field_serializer('genres')
    @classmethod
    def serializer_genres(cls, genres : str) -> list[str]:
        return genres.split('|')
    
    
    @field_serializer('local_link')
    @classmethod
    def movie_id_serialize(cls, local_link : int) -> str:
        zeros_count : int = 7 - len(str(local_link))
        
        return f'search/{"0" * zeros_count}{local_link}'
    
    
    
    
    
    
