from fastapi import APIRouter, Request, Depends, Path, Query
from pydantic import PositiveInt
from typing import Annotated
from core.schemas import MAX_MOVIE_ID, MAX_REVIEW_COUNT, UserActionOut, SuccessUserActionStatusType
from core.models.postgres import StatementReviewType
from .dao import ModeratorRewivewDAO
from .schemas import DeleteReviewIn, ReviewMovieWithUserInfoAndMovieIDOut
from .errors import ModeratorReviewException


router = APIRouter(prefix = '/review', tags = ['Рецензии фильмов'])



@router.get(path = '/get-all', summary = 'Получить все рецензии')
async def get_all_reviews(
                        statement : Annotated[StatementReviewType | None, Query(description = 'Сортировка по типу рецензий')] = None,
                        limit : Annotated[PositiveInt, Query(le = MAX_REVIEW_COUNT, description = 'Максимальное число рецензий')] = MAX_REVIEW_COUNT,
                        offset : Annotated[PositiveInt | None, Query(le = MAX_MOVIE_ID, description = 'Количество последних рецензий, которые нужно пропустить')] = None,
                    ) -> list[ReviewMovieWithUserInfoAndMovieIDOut]:
    return await ModeratorRewivewDAO.get_all_reviews(limit = limit, offset = offset, statement = statement)



@router.post(path = '/delete', summary = 'Удалить рецензию', responses = ModeratorReviewException.get_responses_schemas())
async def delete_review(delete_form : DeleteReviewIn) -> UserActionOut:
    
    await ModeratorRewivewDAO.delete_review(delete_form)
    return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_DELETE)