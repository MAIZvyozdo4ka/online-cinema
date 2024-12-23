from core.models.postgres.Movie import MovieDB
from core.models.postgres.Rating import RatingDB
from core.models.postgres.TrainRatings import TrainRatingsDB
from core.models.postgres.Recommendation import RecommedationDB
from core.models.postgres.User import UserDB
import pandas as pd
from core.dao import PostgresDAO, AsyncSession
from core.dao.recommendation import MovieRecommender
import asyncio
from sqlalchemy import insert, select, update
from typing import List


class RecDAO(PostgresDAO):
    @classmethod
    @PostgresDAO.get_session()
    async def get_movies(cls,
                         session : AsyncSession):
        query = select(MovieDB.id, MovieDB.title, MovieDB.genres)
        movies = await session.execute(query)
        # movies = movies.all()
        df_movies = pd.DataFrame(movies, columns=['id', 'title', 'genres'])
        return df_movies


    @classmethod
    @PostgresDAO.get_session()
    async def get_users(cls,
                        session : AsyncSession):
        query = select(RatingDB.user_id, RatingDB.movie_id, RatingDB.rating)
        users = await session.execute(query)
        # users = users.all()
        df_users = pd.DataFrame(users, columns=['user_id', 'movie_id', 'rating'])
        return df_users

    @classmethod
    @PostgresDAO.get_session()
    async def get_dataset(cls,
                        session: AsyncSession):
        query = select(TrainRatingsDB.user_id, TrainRatingsDB.movie_id, TrainRatingsDB.rating)
        dataset = await session.execute(query)
        # dataset = dataset.all()
        df_dataset = pd.DataFrame(dataset, columns=['user_id', 'movie_id', 'rating'])
        return df_dataset


    @classmethod
    @PostgresDAO.get_session()
    async def get_users_id(cls,
                           session : AsyncSession):
        query = select(UserDB.id)
        users_id = await session.execute(query)
        users_id = users_id.all()

        return users_id


    @classmethod
    @PostgresDAO.get_session()
    async def update(cls,
               session : AsyncSession,
               user_id : int,
               recommendation : List[int]):
        user = await session.get(RecommedationDB, user_id)
        if user:
            user.recommedation = recommendation
            await session.commit()


    def recommendation(self, user_id, df_movies, df_dataset, df_users):
        recommender = MovieRecommender(df_users, df_dataset, df_movies)
        recommendations = recommender.recommend(user_id=user_id)
        return recommendations


async def main():
    users_id = await RecDAO.get_users_id()
    df_users = await RecDAO.get_users()
    df_dataset = pd.read_csv("recommendation-updating/new_clear_rating_with_title.csv")
    df_movies = pd.read_csv("recommendation-updating/movie.csv")
    for id in users_id:
        rec = RecDAO().recommendation(id[0], df_movies, df_dataset, df_users.copy())
        await RecDAO.update(user_id=id[0], recommendation=rec)


if __name__ == "__main__":
    asyncio.run(main())
