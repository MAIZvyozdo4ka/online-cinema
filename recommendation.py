import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from config import *

class MovieRecommender:
    def __init__(self, user_file, dataset_file, movie_file):
        self.my_users = pd.read_csv(user_file)
        self.my_users['userId'] = self.my_users['userId'].apply(lambda x: f"my_{x}")
        dataset_users = pd.read_csv(dataset_file)
        self.user_data = pd.concat([self.my_users, dataset_users], ignore_index=True)
        self.movie_data = pd.read_csv(movie_file)

    def get_genre_score(self, user_id):
        user_movie_matrix = self.user_data.pivot_table(index='userId', columns='movieId', values='rating')
        user_movie_matrix = user_movie_matrix.fillna(0)
        genres_df = self.movie_data['genres'].str.get_dummies('|')
        genres_df['movieId'] = self.movie_data['movieId']
        genres_df.set_index('movieId', inplace=True)
        this_user_rating = user_movie_matrix.loc[user_id]
        this_user_rating = this_user_rating.reset_index()
        this_user_rating.columns = ['movieId', 'rating']
        this_user_rating = this_user_rating.set_index('movieId')[['rating']]
        present_movie_ids_list = this_user_rating.index.tolist()
        filtered_genres_df = genres_df.loc[genres_df.index.isin(present_movie_ids_list)]
        similarity_matrix = cosine_similarity(filtered_genres_df)
        genre_similarity_df = pd.DataFrame(similarity_matrix, index=filtered_genres_df.index, columns=filtered_genres_df.index)
        genre_score = genre_similarity_df @ this_user_rating
        return genre_score


    def get_user_score(self, user_id):
        user_movie_matrix = self.user_data.pivot_table(index='userId', columns='movieId', values='rating')
        user_movie_matrix = user_movie_matrix.fillna(0)
        similarity_matrix = cosine_similarity(user_movie_matrix)
        similarity_df = pd.DataFrame(similarity_matrix, index=user_movie_matrix.index, columns=user_movie_matrix.index)
        this_user_similarity = similarity_df.loc[user_id]
        this_user_similarity = this_user_similarity.reset_index()
        this_user_similarity.columns = ['user_id', 'similarity']
        this_user_similarity = this_user_similarity.set_index('user_id')[['similarity']]
        score = this_user_similarity.T @ user_movie_matrix
        return score.T
    
    def get_default_recommendations(self, top_n=10):
        movie_ratings = self.user_data.groupby('movieId')['rating'].agg(['mean', 'count'])
        movie_ratings.columns = ['average_rating', 'rating_count']
        popular_movies = self.movie_data.merge(movie_ratings, on='movieId')
        popular_movies = popular_movies.sort_values(by=['average_rating', 'rating_count'], ascending=[False, False])
        default_recommendations = popular_movies[['title', 'genres']].head(top_n)
        return default_recommendations
    
    def recommend(self, user_id, top_n=10):
        user_id = "my_" + str(user_id)
        if not ( user_id in self.my_users['userId'].values):
            return  self.get_default_recommendations(top_n)
        genre_score = self.get_genre_score(user_id)
        user_score = self.get_user_score(user_id)
        scaler = MinMaxScaler()
        user_score['similarity'] = scaler.fit_transform(user_score[['similarity']])
        genre_score['rating'] = scaler.fit_transform(genre_score[['rating']])
        result = (genre_score.iloc[:, 0]) + (user_score.iloc[:, 0])
        result_df = result.to_frame(name='combined_score')
        
        sorted_df = result_df.sort_values(by='combined_score', ascending=False)
        watched_movies = self.my_users.loc[self.my_users['userId'] == user_id, 'movieId']
        watched_movies_list = watched_movies.tolist()
        filtered_df = sorted_df[~sorted_df.index.isin(watched_movies_list)]
        cutted_df = filtered_df.head(40)

        recommended_movies = cutted_df.merge(self.movie_data, left_index=True, right_on='movieId')
        recommended_movies = recommended_movies[['title', 'genres', 'combined_score']]
        return recommended_movies.head(top_n)

recommender = MovieRecommender(user_file, dataset_file, movie_file)

if __name__ == "__main__":
    # Пример использования
    user_id = "1"
    recommendations = recommender.recommend(user_id=user_id)
    print(f"Рекомендации для пользователя {user_id}:")
    print(recommendations)