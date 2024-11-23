import pandas as pd
def filter_and_save(dataset_file, output_file, min_user_ratings=50, min_movie_ratings=100):
    """
    Фильтрует данные, оставляя только активных пользователей датасета и популярные фильмы, и сохраняет результат в новый CSV.
    """

    user_data = pd.read_csv(dataset_file).drop(columns=['timestamp'])
    movie_ratings_count = user_data['movieId'].value_counts()
    popular_movies = movie_ratings_count[movie_ratings_count >= min_movie_ratings].index

    user_ratings_count = user_data['userId'].value_counts()
    active_users = user_ratings_count[user_ratings_count >= min_user_ratings].index

    filtered_data = user_data[
        (user_data['movieId'].isin(popular_movies)) &
        (user_data['userId'].isin(active_users))
    ]
    filtered_data.to_csv(output_file, index=False)


if __name__ == "__main__":
    filter_and_save(
        dataset_file='dataset/rating.csv',
        output_file='filtered_data.csv',
        min_user_ratings=500,
        min_movie_ratings=100
    )
