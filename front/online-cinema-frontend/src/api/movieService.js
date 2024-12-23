import apiClient from './apiClient';

export const getMovies = async () => {
    const response = await apiClient.get('/');
    return response.data;
};

export const getMovieDetails = async (movieId) => {
    const response = await apiClient.get(`/${movieId}`);
    return response.data;
};
