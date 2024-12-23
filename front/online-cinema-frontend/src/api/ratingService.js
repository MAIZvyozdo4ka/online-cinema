import apiClient from './apiClient';

export const getRatings = async () => {
    const response = await apiClient.get('/rating');
    return response.data;
};
