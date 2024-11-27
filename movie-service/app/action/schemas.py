from core.schemas.movie import MovieModelOut, BaseModel
from pydantic import Field, ConfigDict, field_serializer



class LinksForAnotherSiteModel(BaseModel):
    
    imdb_link : int | None = Field(default = None, validation_alias = 'imdb_id', description = 'Ссылка на IMDB')
    tmbd_link : int | None = Field(default = None, validation_alias = 'tmbd_id', description = 'Ссылка на TMDB')
    
    model_config = ConfigDict(title = 'Cсылки на другие сайты')
    
    
    
    
class LinksForAnotherSiteOut(LinksForAnotherSiteModel):
    
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
  
  


class MovieOut(MovieModelOut):
    links : LinksForAnotherSiteOut = Field(description = 'Ссылки на фильм', validation_alias = 'link')
    
    model_config = ConfigDict(title = 'Полная инормация о фильме')
    
    