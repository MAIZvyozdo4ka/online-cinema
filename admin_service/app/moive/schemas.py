from core.schemas import LinksForAnotherSite, MovieModel, MovieID, BaseModel
from pydantic import Field, AnyUrl, field_serializer, ConfigDict


class MovieModelIn(MovieModel):
    @field_serializer('genres')
    @classmethod
    def genres_field_serializer(cls, genres : list[str]) -> str:
        return '|'.join(genres)


class MovieModelWithNoneFields(MovieModelIn):
    title : str | None = Field(description = 'Назавние фильма', min_length = 1, default = None)
    description : str | None = Field(description = 'Описание фильма', min_length = 1, default = None)
    genres : list[str] | None = Field(description = 'Жанры фильма', min_length = 1, default = None)
    
    
    
class LinksForAnotherSiteIn(LinksForAnotherSite):
    imdb_link : AnyUrl | None = Field(default = None,
                                      serialization_alias = 'imdb_id',
                                      description = 'Ссылка на IMDB',
                                      examples = ['https://www.imdb.com/title/tt0000001']
                                    )
    tmbd_link : AnyUrl | None = Field(default = None,
                                      serialization_alias = 'tmbd_id',
                                      description = 'Ссылка на TMDB',
                                      examples = ['https://www.themoviedb.org/movie/1']
                                    )
    
    model_config = ConfigDict(title = 'Cсылки на другие сайты')
    
    
    @field_serializer('imdb_link')
    @classmethod
    def imdb_link_field_serializer(cls, imdb_link : AnyUrl | None) -> int | None:
        if imdb_link is None:
            return None
        return int(imdb_link.path.rsplit('/', 1)[1].removeprefix('tt'))
    
    
    @field_serializer('tmbd_link')
    @classmethod
    def tmbd_link_field_serializer(cls, tmbd_link : AnyUrl | None) -> int | None:
        if tmbd_link is None:
            return None
        return int(tmbd_link.path.rsplit('/', 1)[1])
    
    
    

        
class UpdateMoiveIn(MovieModelWithNoneFields):
    id : MovieID = Field(description = 'ID фильма', exclude = True)
    links : LinksForAnotherSiteIn = Field(default = None, exclude = True)
    
    model_config = ConfigDict(title = 'Форма для обновления фильма')
    
    


class NewMovieIn(MovieModelIn):
    links : LinksForAnotherSiteIn = Field(exclude = True)
    
    model_config = ConfigDict(title = 'Форма для создания фильма')
    
    
    
    