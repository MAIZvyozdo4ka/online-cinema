import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid,
} from 'recharts';

function MoviePage() {
    const { movieId } = useParams();
    const [movie, setMovie] = useState(null);
    const [error, setError] = useState(null);
    const [reviewError, setReviewError] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const [ratingMessage, setRatingMessage] = useState(null);
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const [header, setHeader] = useState('');
    const [review, setReview] = useState('');
    const [statement, setStatement] = useState('positive');

    // New state variables
    const [ratingsDistribution, setRatingsDistribution] = useState([]);
    const [myRating, setMyRating] = useState(null);
    const [reviewsData, setReviewsData] = useState({
        reviews: [],
        reviews_count: 0,
        positive_statement_percent: 0,
        negative_statement_percent: 0,
        neutral_statement_percent: 0,
    });
    const [myReview, setMyReview] = useState(null);

    // Validation states
    const [headerValid, setHeaderValid] = useState(false);
    const [reviewValid, setReviewValid] = useState(false);

    // Fetch movie details
    useEffect(() => {
        const fetchMovie = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/movie/${movieId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || 'Failed to fetch movie details');
                }

                const data = await response.json();
                setMovie(data);
                setError(null);
            } catch (err) {
                setError(err.message);
                setMovie(null);
            }
        };

        fetchMovie();
    }, [movieId, API_BASE_URL]);

    // Fetch user's own review
    const fetchMyReview = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/review/movie/${movieId}/my`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.status === 401) {
                setMyReview(null);
                return;
            }

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to fetch your review');
            }

            const data = await response.json();
            setMyReview(data);
        } catch (err) {
            console.error(err.message);
            setMyReview(null); // Ensure it's set to null on error
        }
    };

    useEffect(() => {
        fetchMyReview();
    }, [movieId, API_BASE_URL]);

    // Fetch reviews
    const fetchReviews = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/review/movie/${movieId}?limit=10`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to fetch reviews');
            }

            const data = await response.json();
            setReviewsData({
                reviews: Array.isArray(data.reviews) ? data.reviews : [],
                reviews_count: data.reviews_count || 0,
                positive_statement_percent: data.positive_statement_percent || 0,
                negative_statement_percent: data.negative_statement_percent || 0,
                neutral_statement_percent: data.neutral_statement_percent || 0,
            });
        } catch (err) {
            console.error(err.message);
            setReviewsData({
                reviews: [],
                reviews_count: 0,
                positive_statement_percent: 0,
                negative_statement_percent: 0,
                neutral_statement_percent: 0,
            });
        }
    };

    useEffect(() => {
        fetchReviews();
    }, [movieId, API_BASE_URL]);

    // Fetch ratings distribution
    useEffect(() => {
        const fetchRatingsDistribution = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/rating/movie/${movieId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || 'Failed to fetch ratings distribution');
                }

                const data = await response.json();
                setRatingsDistribution(Array.isArray(data) ? data : []);
            } catch (err) {
                console.error(err.message);
                setRatingsDistribution([]); // Ensure it's an array even on error
            }
        };

        fetchRatingsDistribution();
    }, [movieId, API_BASE_URL]);

    // Fetch user's own rating
    useEffect(() => {
        const fetchMyRating = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/rating/movie/${movieId}/my`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (response.status === 401) {
                    setMyRating(null);
                    return;
                }

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || 'Failed to fetch your rating');
                }

                const data = await response.json();
                setMyRating(data.rating);
            } catch (err) {
                console.error(err.message);
                setMyRating(null); // Ensure it's set to null on error
            }
        };

        fetchMyRating();
    }, [movieId, API_BASE_URL]);

    // Validate header
    useEffect(() => {
        if (header && header.length >= 10 && header.length <= 100) {
            setHeaderValid(true);
        } else {
            setHeaderValid(false);
        }
    }, [header]);

    // Validate review
    useEffect(() => {
        if (review && review.length > 10) {
            setReviewValid(true);
        } else {
            setReviewValid(false);
        }
    }, [review]);

    const handleReviewSubmit = async (e) => {
        e.preventDefault();

        if (!headerValid || !reviewValid) {
            setReviewError('Please ensure all fields meet the validation criteria.');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/review/review-movie`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    movie_id: Number(movieId),
                    header,
                    review,
                    statement,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to submit review');
            }

            setSuccessMessage('Ваш отзыв успешно отправлен!');
            setReviewError(null);
            setHeader('');
            setReview('');
            setStatement('positive');

            // Refresh data
            fetchMyReview();
            fetchReviews();
        } catch (err) {
            setReviewError(err.message);
            setSuccessMessage(null);
        }
    };

    if (error) {
        return <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>;
    }

    if (!movie) {
        return <p style={{ textAlign: 'center' }}>Загрузка информации о фильме...</p>;
    }

    return (
        <div style={{ maxWidth: '800px', margin: '50px auto', textAlign: 'center' }}>
            <h1>{movie.title}</h1>
            {movie.poster_url && (
                <img src={movie.poster_url} alt={movie.title} style={{ width: '300px', margin: '20px 0' }} />
            )}
            <p>
                <strong>Жанры:</strong> {movie.genres ? movie.genres.join(', ') : 'Нет жанров'}
            </p>
            <p>
                <strong>Рейтинг:</strong> {movie.rating}
            </p>
            <p>
                <strong>Количество оценок:</strong> {movie.rating_count}
            </p>
            <p>
                <strong>Количество отзывов:</strong> {movie.review_count}
            </p>

            {/* Ratings Distribution Chart */}
            <div style={{ marginTop: '50px' }}>
                <h3>Распределение оценок</h3>
                {ratingsDistribution.length > 0 ? (
                    <BarChart width={600} height={300} data={ratingsDistribution}>
                        <CartesianGrid stroke="#ccc" />
                        <XAxis dataKey="rating" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="rating_count" fill="#8884d8" />
                    </BarChart>
                ) : (
                    <p>Нет данных для отображения распределения оценок.</p>
                )}
            </div>

            {/* User's Own Rating */}
            <div style={{ marginTop: '20px' }}>
                <h3>Моя оценка</h3>
                {myRating !== null ? (
                    <p>Вы поставили оценку: {myRating}</p>
                ) : (
                    <p>Вы ещё не оценили этот фильм.</p>
                )}
            </div>

            {/* User's Own Review */}
            <div style={{ marginTop: '50px' }}>
                <h3>Мой отзыв</h3>
                {myReview ? (
                    <div style={{ textAlign: 'left', border: '1px solid #ccc', padding: '10px', marginBottom: '20px' }}>
                        <h4>{myReview.header}</h4>
                        <p>{myReview.review}</p>
                        <p><strong>Оценка:</strong> {myReview.statement}</p>
                        <p><em>Последнее изменение: {myReview.last_modified}</em></p>
                    </div>
                ) : (
                    <p>Вы ещё не оставили отзыв на этот фильм.</p>
                )}
            </div>

            {/* Leave a Review Form */}
            <div>
                <h3>Оставить отзыв</h3>
                {reviewError && <p style={{ color: 'red' }}>{reviewError}</p>}
                {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
                <form onSubmit={handleReviewSubmit} style={{ marginTop: '20px' }}>
                    <div style={{ marginBottom: '10px', textAlign: 'left' }}>
                        <label>
                            Заголовок (от 10 до 100 символов):
                            <input
                                type="text"
                                value={header}
                                onChange={(e) => setHeader(e.target.value)}
                                style={{ width: '100%', padding: '10px', marginTop: '5px' }}
                                required
                            />
                        </label>
                        {!headerValid && header.length > 0 && (
                            <p style={{ color: 'red', fontSize: '0.9rem' }}>
                                Заголовок должен быть от 10 до 100 символов.
                            </p>
                        )}
                    </div>
                    <div style={{ marginBottom: '10px', textAlign: 'left' }}>
                        <label>
                            Отзыв (больше 10 символов):
                            <textarea
                                value={review}
                                onChange={(e) => setReview(e.target.value)}
                                style={{ width: '100%', padding: '10px', marginTop: '5px', height: '100px' }}
                                required
                            />
                        </label>
                        {!reviewValid && review.length > 0 && (
                            <p style={{ color: 'red', fontSize: '0.9rem' }}>
                                Отзыв должен быть больше 10 символов.
                            </p>
                        )}
                    </div>
                    <div style={{ marginBottom: '10px', textAlign: 'left' }}>
                        <label>
                            Оценка:
                            <div>
                                <label>
                                    <input
                                        type="radio"
                                        name="statement"
                                        value="positive"
                                        checked={statement === 'positive'}
                                        onChange={(e) => setStatement(e.target.value)}
                                    />
                                    Положительный
                                </label>
                                <label style={{ marginLeft: '20px' }}>
                                    <input
                                        type="radio"
                                        name="statement"
                                        value="negative"
                                        checked={statement === 'negative'}
                                        onChange={(e) => setStatement(e.target.value)}
                                    />
                                    Отрицательный
                                </label>
                                <label style={{ marginLeft: '20px' }}>
                                    <input
                                        type="radio"
                                        name="statement"
                                        value="neutral"
                                        checked={statement === 'neutral'}
                                        onChange={(e) => setStatement(e.target.value)}
                                    />
                                    Нейтральный
                                </label>
                            </div>
                        </label>
                    </div>
                    <button
                        type="submit"
                        style={{ padding: '10px', width: '100%', backgroundColor: '#28a745', color: '#fff' }}
                        disabled={!headerValid || !reviewValid}
                    >
                        Отправить отзыв
                    </button>
                </form>
            </div>

            {/* Users' Reviews */}
            <div style={{ marginTop: '50px' }}>
                <h3>Отзывы пользователей</h3>
                <p>Всего отзывов: {reviewsData.reviews_count}</p>
                <p>Положительных: {reviewsData.positive_statement_percent}%</p>
                <p>Отрицательных: {reviewsData.negative_statement_percent}%</p>
                <p>Нейтральных: {reviewsData.neutral_statement_percent}%</p>
                {reviewsData.reviews.length > 0 ? (
                    reviewsData.reviews.map((reviewItem, index) => (
                        <div key={index} style={{ textAlign: 'left', border: '1px solid #ccc', padding: '10px', marginBottom: '20px' }}>
                            <h4>{reviewItem.header}</h4>
                            <p>{reviewItem.review}</p>
                            <p><strong>Оценка:</strong> {reviewItem.statement}</p>
                            <p><strong>Пользователь:</strong> {reviewItem.user.username}</p>
                        </div>
                    ))
                ) : (
                    <p>Нет отзывов для отображения.</p>
                )}
            </div>
        </div>
    );
}

export default MoviePage;
