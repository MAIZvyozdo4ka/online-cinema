import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function AccountPage() {
    const [userInfo, setUserInfo] = useState(null); // Данные пользователя
    const [ratings, setRatings] = useState(null); // Рейтинги фильмов
    const [reviews, setReviews] = useState(null); // Отзывы на фильмы
    const [error, setError] = useState(null); // Ошибки
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL; // Базовый URL API
    const navigate = useNavigate(); // Навигация

    useEffect(() => {
        // Получение информации о пользователе
        const fetchUserInfo = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/me/account`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                    },
                });

                if (response.status === 401) {
                    localStorage.removeItem('accessToken');
                    navigate('/login');
                    throw new Error('Unauthorized: Redirecting to login page');
                }

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || 'Failed to fetch user info');
                }

                const data = await response.json();
                setUserInfo(data);
            } catch (err) {
                setError(err.message);
            }
        };

        // Получение рейтингов фильмов
        const fetchRatings = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/rating/my`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || 'Failed to fetch ratings');
                }

                const data = await response.json();
                setRatings(data.rate_list);
            } catch (err) {
                setError(err.message);
            }
        };

        // Получение отзывов на фильмы
        const fetchReviews = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/review/my`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || 'Failed to fetch reviews');
                }

                const data = await response.json();
                setReviews(data.reviews_list);
            } catch (err) {
                setError(err.message);
            }
        };

        fetchUserInfo();
        fetchRatings();
        fetchReviews();
    }, [API_BASE_URL]);

    if (error) {
        return <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>;
    }

    if (!userInfo) {
        return <p style={{ textAlign: 'center' }}>Loading user information...</p>;
    }

    return (
        <div style={{ maxWidth: '800px', margin: '50px auto', textAlign: 'center' }}>
            <h1>Account Information</h1>
            <p><strong>First Name:</strong> {userInfo.first_name}</p>
            <p><strong>Last Name:</strong> {userInfo.last_name}</p>
            <p><strong>Email:</strong> {userInfo.email}</p>

            <div style={{ marginTop: '20px' }}>
                <button
                    onClick={() => navigate('/logout')}
                    style={{
                        padding: '10px 20px',
                        fontSize: '16px',
                        backgroundColor: '#f44336',
                        color: '#fff',
                        border: 'none',
                        cursor: 'pointer',
                        marginRight: '10px',
                    }}
                >
                    Logout
                </button>
                <button
                    onClick={() => navigate('/full-logout')}
                    style={{
                        padding: '10px 20px',
                        fontSize: '16px',
                        backgroundColor: '#ff9800',
                        color: '#fff',
                        border: 'none',
                        cursor: 'pointer',
                    }}
                >
                    Logout from All Devices
                </button>
            </div>

            <div style={{ marginTop: '40px' }}>
                <h2>Your Ratings</h2>
                {!ratings ? (
                    <p>Loading your ratings...</p>
                ) : (
                    ratings.map((rating, index) => (
                        <div key={index} style={{ textAlign: 'left', marginBottom: '10px' }}>
                            <strong>Movie:</strong> {rating.movie.title} <br />
                            <strong>Genres:</strong> {rating.movie.genres.join(', ')} <br />
                            <strong>Rating:</strong> {rating.rating} <br />
                            <strong>Last Modified:</strong> {rating.last_modified} <br />
                        </div>
                    ))
                )}
            </div>

            <div style={{ marginTop: '40px' }}>
                <h2>Your Reviews</h2>
                {!reviews ? (
                    <p>Loading your reviews...</p>
                ) : (
                    reviews.map((review, index) => (
                        <div key={index} style={{ textAlign: 'left', marginBottom: '10px' }}>
                            <strong>Movie:</strong> {review.movie.title} <br />
                            <strong>Genres:</strong> {review.movie.genres.join(', ')} <br />
                            <strong>Header:</strong> {review.header} <br />
                            <strong>Review:</strong> {review.review} <br />
                            <strong>Statement:</strong> {review.statement} <br />
                            <strong>Last Modified:</strong> {review.last_modified} <br />
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}

export default AccountPage;
