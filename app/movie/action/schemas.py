from app.movie.schemas import MovieModelOut
from pydantic import Field, ConfigDict, field_serializer, PositiveInt, computed_field
from app.BaseModel import BaseModel
from app.user.schemas import NonPrivateUserInfoOut
from app.user.movie_action.schemas import UserActionMovie, ReviewMovie, RateMovie, UserMoiveActionsInfo




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
    
    
    
 
class ReviewMovieWithUserInfoOut(UserActionMovie, ReviewMovie):
    user : NonPrivateUserInfoOut
    
    model_config = ConfigDict(title = 'Рецензии фильма')
    
    
    
    
class MovieWithUserInfoOut(BaseModel):
    movie : MovieOut 
    user_info : UserMoiveActionsInfo | None = Field(default = None)
    reviews : list[ReviewMovieWithUserInfoOut] = Field(description = 'Последние рецензии')
    
    model_config = ConfigDict(title = 'Полная инормация о фильме c мнением пользователя')
    
    

class ReviewMovieWithUserInfoListWithStatisticOut(BaseModel):
    reviews : list[ReviewMovieWithUserInfoOut] = Field(description = 'Последние рецензии')
    reviews_count : int = Field(description = 'Количество рецензий фильма')
    positive_statement_percent : float = Field(description = 'Процент положительных рецензий фильма')
    negative_statement_percent : float = Field(description = 'Процент негативных рецензий фильма')
    neutral_statement_percent : float = Field(description = 'Процент нейтральных рецензий фильма')
    
    model_config = ConfigDict(title = 'Рецензии фильма со статистикой')
    
    

class MovieRatingOut(RateMovie):
    rating_count : PositiveInt = Field(description = 'Количество оценок')
    
    model_config = ConfigDict(title = 'Статистика оценок фильма')
    