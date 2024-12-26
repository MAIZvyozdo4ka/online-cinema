from core.schemas import MovieModelOut, LinksForAnotherSite, is_movie_id
from pydantic import Field, ConfigDict, field_validator, AnyUrl
from typing import Any
    
    
class LinksForAnotherSiteOut(LinksForAnotherSite):
    
    
    @field_validator('tmbd_link', mode = 'before')
    @classmethod
    def tmdb_link_validator(cls, tmbd_id : Any) -> AnyUrl | None:
        if isinstance(tmbd_id, int) and is_movie_id(tmbd_id):
            return AnyUrl(f'https://www.themoviedb.org/movie/{tmbd_id}')
        return super().tmdb_link_validator(tmbd_id)
    
    
    @field_validator('imdb_link', mode = 'before')
    @classmethod
    def imdb_link_validator(cls, imdb_id : Any) -> AnyUrl | None:
        if isinstance(imdb_id, int) and is_movie_id(imdb_id):
            zero_count : int = 7 - len(str(imdb_id))
            return AnyUrl(f'https://www.imdb.com/title/tt{"0" * zero_count}{imdb_id}')
        return super().imdb_link_validator(imdb_id)
  


class MovieOut(MovieModelOut):
    links : LinksForAnotherSiteOut = Field(description = 'Ссылки на фильм', validation_alias = 'link')
    
    model_config = ConfigDict(title = 'Полная инормация о фильме')
    
    