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
                         session : AsyncSession,
                         batch_size: int = 1000):
        query = select(MovieDB.id, MovieDB.title, MovieDB.genres)
        result = await session.stream(query)  # Асинхронный стриминг данных

        df_movies = pd.DataFrame(columns=['id', 'title', 'genres'])

        while True:
            rows = await result.fetchmany(batch_size)
            if not rows:
                break

            batch_df = pd.DataFrame(rows, columns=['id', 'title', 'genres'])
            df_movies = pd.concat([df_movies, batch_df], ignore_index=True)

        return df_movies


    @classmethod
    @PostgresDAO.get_session()
    async def get_users(cls,
                        session : AsyncSession,
                        batch_size: int = 1000):
        query = select(RatingDB.user_id, RatingDB.movie_id, RatingDB.rating)
        result = await session.stream(query)  # Асинхронный стриминг данных

        df_users = pd.DataFrame(columns=['user_id', 'movie_id', 'rating'])

        while True:
            rows = await result.fetchmany(batch_size)
            if not rows:
                break

            batch_df = pd.DataFrame(rows, columns=['user_id', 'movie_id', 'rating'])
            df_users = pd.concat([df_users, batch_df], ignore_index=True)

        return df_users

    @classmethod
    @PostgresDAO.get_session()
    async def get_dataset(cls,
                        session: AsyncSession,
                        batch_size: int = 1000):
        query = select(TrainRatingsDB.user_id, TrainRatingsDB.movie_id, TrainRatingsDB.rating)
        result = await session.stream(query)

        df_dataset = pd.DataFrame(columns=['user_id', 'movie_id', 'rating'])

        while True:
            rows = await result.fetchmany(batch_size)
            if not rows:
                break

            batch_df = pd.DataFrame(rows, columns=['user_id', 'movie_id', 'rating'])
            df_dataset = pd.concat([df_dataset, batch_df], ignore_index=True)

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
    df_dataset = await RecDAO.get_dataset()
    df_movies = await RecDAO.get_movies()
    for id in users_id:
        rec = RecDAO().recommendation(id[0], df_movies, df_dataset, df_users.copy())
        await RecDAO.update(user_id=id[0], recommendation=rec)


if __name__ == "__main__":
    asyncio.run(main())
