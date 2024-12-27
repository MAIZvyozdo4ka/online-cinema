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
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const [header, setHeader] = useState('');
    const [review, setReview] = useState('');
    const [statement, setStatement] = useState('positive');

    const [ratingsDistribution, setRatingsDistribution] = useState([]);
    const [myRating, setMyRating] = useState(null);
    const [selectedRating, setSelectedRating] = useState(null);
    const [reviewsData, setReviewsData] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [myReview, setMyReview] = useState(null);

    const [headerValid, setHeaderValid] = useState(false);
    const [reviewValid, setReviewValid] = useState(false);

    useEffect(() => {
        const fetchAllData = async () => {
            try {
                // Fetch movie details
                const fetchMovie = async () => {
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
                };

                // Fetch user's own review
                const fetchMyReview = async () => {
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
                };

                // Fetch reviews
                const fetchReviews = async () => {
                    const response = await fetch(`${API_BASE_URL}/review/movie/${movieId}`);
                    if (!response.ok) {
                        throw new Error('Failed to fetch reviews');
                    }
                    const data = await response.json();
                    setReviewsData(data);
                    setReviews(data.reviews || []);
                };

                // Fetch ratings distribution
                const fetchRatingsDistribution = async () => {
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
                };

                // Fetch user's own rating
                const fetchMyRating = async () => {
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
                    setMyRating(data?.rating ?? null);
                };

                // Выполняем все запросы параллельно
                await Promise.all([
                    fetchMovie(),
                    fetchMyReview(),
                    fetchReviews(),
                    fetchRatingsDistribution(),
                    fetchMyRating(),
                ]);

                setError(null);
            } catch (err) {
                console.error(err.message);
                setError(err.message);
            }
        };

        fetchAllData();
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

    const handleRatingSubmit = async (rating) => {
        try {
            const response = await fetch(`${API_BASE_URL}/rating/rate-movie`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    movie_id: Number(movieId),
                    rating,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to submit rating');
            }

            setSelectedRating(rating);
            setMyRating(rating);
        } catch (err) {
            console.error('Ошибка при отправке оценки:', err.message);
        }
    };

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
        } catch (err) {
            setReviewError(err.message);
            setSuccessMessage(null);
        }
    };

    if (error) {
        return (
            <div style={{ textAlign: 'center', padding: '50px' }}>
                <h1>Что-то пошло не так</h1>
                <p style={{ color: 'red' }}>{error}</p>
                <p>Попробуйте обновить страницу или вернуться позже.</p>
            </div>
        );
    }

    if (!movie) {
        return (
            <div style={{ textAlign: 'center', padding: '50px' }}>
                <h1>Загрузка...</h1>
                <p>Пожалуйста, подождите, информация о фильме загружается.</p>
            </div>
        );
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

            {/* Video Player */}
            <div style={{ marginTop: '20px' }}>
                <h3>Просмотр фильма</h3>
                <video
                    width="600"
                    controls
                    src={`${API_BASE_URL}/movie/${movieId}/play`}
                    style={{ marginTop: '20px' }}
                >
                    Ваш браузер не поддерживает видео.
                </video>
            </div>

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
                <div style={{ marginTop: '10px' }}>
                    <p>Поставьте оценку фильму (1-10):</p>
                    <div style={{ display: 'flex', justifyContent: 'center', gap: '5px' }}>
                        {[...Array(10)].map((_, index) => {
                            const ratingValue = index + 1;
                            return (
                                <button
                                    key={ratingValue}
                                    onClick={() => handleRatingSubmit(ratingValue)}
                                    style={{
                                        padding: '10px',
                                        backgroundColor: ratingValue === selectedRating ? '#28a745' : '#ddd',
                                        color: ratingValue === selectedRating ? '#fff' : '#000',
                                        border: 'none',
                                        cursor: 'pointer',
                                        borderRadius: '5px',
                                    }}
                                >
                                    {ratingValue}
                                </button>
                            );
                        })}
                    </div>
                </div>
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
            <div style={{ marginTop: '50px', textAlign: 'center' }}>
                <h2>Отзывы</h2>

                {/* Статистика отзывов */}
                {reviewsData && (
                    <div>
                        <p>Всего отзывов: {reviewsData.reviews_count}</p>
                        <p>Положительных: {reviewsData.positive_statement_percent}%</p>
                        <p>Нейтральных: {reviewsData.neutral_statement_percent}%</p>
                        <p>Негативных: {reviewsData.negative_statement_percent}%</p>
                    </div>
                )}

                {/* Список отзывов */}
                {reviewsData.reviews.length > 0 ? (
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                        {reviews.map((review, index) => (
                            <li
                                key={index}
                                style={{
                                    marginBottom: '20px',
                                    borderBottom: '1px solid #ccc',
                                    paddingBottom: '10px',
                                    textAlign: 'left',
                                }}
                            >
                                <h3>{review.header}</h3>
                                <p>{review.review}</p>
                                <p><strong>Тональность:</strong> {review.statement}</p>
                                <p><strong>Автор:</strong> {review.user.username}</p>
                                <p><strong>Последнее изменение:</strong> {review.last_modified}</p>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>Отзывов пока нет.</p>
                )}
            </div>


        </div>
    );
}

export default MoviePage;