from pydantic import Field, ConfigDict, computed_field, AnyUrl, AliasChoices, field_validator, PositiveInt
from .BaseModel import BaseModel
from typing import Any, Annotated 
import annotated_types



MAX_MOVIE_ID : int = 10_000_000
MovieID = Annotated[PositiveInt, annotated_types.Le(MAX_MOVIE_ID)]


def is_movie_id(id : int) -> bool:
    return 0 <= id <= MAX_MOVIE_ID



class MovieModel(BaseModel):
    title : str = Field(description = 'Назавние фильма', min_length = 1)
    description : str = Field(description = 'Описание фильма', min_length = 1)
    genres : list[str] = Field(description = 'Жанры фильма', min_length = 1)
    
    @field_validator('genres', mode = 'after')
    @classmethod
    def validator_genres(cls, genres : list[str]) -> list[str]:

        if any(map(lambda genre : len(genre) < 1, genres)):
            raise ValueError('genre too short')
        
        return genres



class MovieModelOut(MovieModel):
    
    id : int = Field(exclude = True)
    rating : float = Field(description = 'Средняя оценка фильма', validation_alias = 'movie_rating_avg')
    rating_count : int = Field(description = 'Количество оценок фильма', validation_alias = 'movie_rating_count')
    review_count : int = Field(description = 'Количество рецензий фильма', validation_alias = 'movie_reviews_count')
    
    model_config = ConfigDict(title = 'Информация о фильме')
    
    @computed_field(description = 'Ссылка для открытия фильма')
    @property
    def local_link(self) -> str:
        zeros_count : int = 7 - len(str(self.id))
        
        return f'/api/v1/movie/{"0" * zeros_count}{self.id}'
    
    
    @field_validator('genres', mode = 'before')
    @classmethod
    def validator_genres(cls, genres : Any) -> list[str]:
        if not isinstance(genres, str):
            raise ValueError('genres has incorrect type')
        
        return super().validator_genres(genres.split('|'))
    
    
    
class LinksForAnotherSite(BaseModel):
    imdb_link : AnyUrl | None = Field(default = None,
                                      validation_alias = AliasChoices('imdb_link', 'imdb_id'),
                                      description = 'Ссылка на IMDB',
                                      examples = ['https://www.imdb.com/title/tt0000001']
                                    )
    tmbd_link : AnyUrl | None = Field(default = None,
                                      validation_alias = AliasChoices('tmbd_link', 'tmbd_id'),
                                      description = 'Ссылка на TMDB',
                                      examples = ['https://www.themoviedb.org/movie/1']
                                    )
    
    model_config = ConfigDict(title = 'Cсылки на другие сайты')
    
    
    
    @field_validator('tmbd_link', mode = 'after')
    @classmethod
    def tmdb_link_validator(cls, tmbd_link : AnyUrl | None) -> AnyUrl | None:
        if tmbd_link is None:
            return None
        
        if tmbd_link.host != 'www.themoviedb.org':
            raise ValueError('tmbd_link has incorrect hostname')
        
        tmbd_id : str = tmbd_link.path.rsplit('/', 1)[1]
        
        if not (tmbd_id.isnumeric() and is_movie_id(int(tmbd_id))):
            raise ValueError('tmbd_link is minus or too long')
            
        return tmbd_link
            
            
    
    @field_validator('imdb_link', mode = 'after')
    @classmethod
    def imdb_link_validator(cls, imdb_link : AnyUrl | None) -> AnyUrl | None:
        if imdb_link is None:
            return None
        
        if imdb_link.host != 'www.imdb.com':
            raise ValueError(str(imdb_link.host))
        
        imdb_id : str = imdb_link.path.rsplit('/', 1)[1].removeprefix('tt')
        if not (imdb_id.isnumeric() and is_movie_id(int(imdb_id))):
            raise ValueError('imdb_link is minus or too long')
            
        return imdb_link
  
        
    
    
    
    
    