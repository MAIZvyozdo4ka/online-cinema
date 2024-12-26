import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
    const [searchQuery, setSearchQuery] = useState('');
    const [movies, setMovies] = useState([]);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
    const navigate = useNavigate();

    const handleSearch = async (e) => {
        e.preventDefault();
        if (searchQuery.trim().length < 3) {
            setError('Search query must be at least 3 characters long.');
            setMovies([]);
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch(`${API_BASE_URL}/search?text=${encodeURIComponent(searchQuery)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                const errorMessage = errorData.ditail
                    ? `${errorData.ditail.type}: ${errorData.ditail.message}`
                    : 'Failed to fetch movies';
                throw new Error(errorMessage);
            }

            const data = await response.json();
            setMovies(data);
        } catch (err) {
            setError(err.message);
            setMovies([]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleWatchNow = (movie) => {
        const token = localStorage.getItem('accessToken');
        if (!token) {
            navigate('/login');
            return;
        }
        const movieId = parseInt(movie.local_link.replace('/api/v1/movie/', ''), 10);
        navigate(`/movie/${movieId}`);
    };

    const handleProfileNavigation = () => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            navigate('/account');
        } else {
            navigate('/login');
        }
    };

    return (
        <div className="homepage">
            <header className="homepage-header">
                <h1>Search for Movies</h1>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <form onSubmit={handleSearch} style={{ flex: 1 }}>
                        <input
                            type="text"
                            placeholder="Enter movie title..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            style={{
                                width: '60%',
                                padding: '10px',
                                fontSize: '16px',
                                marginRight: '10px',
                            }}
                            required
                        />
                        <button
                            type="submit"
                            style={{
                                padding: '10px 20px',
                                fontSize: '16px',
                                backgroundColor: '#007bff',
                                color: '#fff',
                                border: 'none',
                                cursor: 'pointer',
                            }}
                        >
                            Search
                        </button>
                    </form>
                    <button
                        onClick={handleProfileNavigation}
                        style={{
                            marginLeft: '10px',
                            padding: '10px 20px',
                            fontSize: '16px',
                            backgroundColor: '#28a745',
                            color: '#fff',
                            border: 'none',
                            cursor: 'pointer',
                        }}
                    >
                        {localStorage.getItem('accessToken') ? 'Profile' : 'Login'}
                    </button>
                </div>
            </header>

            {isLoading && <p style={{ textAlign: 'center', color: '#007bff' }}>Loading...</p>}
            {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

            <section className="movie-results" style={{ marginTop: '20px' }}>
                {movies.length > 0 ? (
                    <div className="movie-list">
                        {movies.map((movie, index) => {
                            const movieId = movie.local_link.replace('/api/v1/movie/', '');
                            return (
                                <div key={index} className="movie-item" style={{ marginBottom: '20px' }}>
                                    <h2>{movie.title}</h2>
                                    <p><strong>Genres:</strong> {movie.genres.join(', ')}</p>
                                    <p><strong>Rating:</strong> {movie.rating} ({movie.rating_count} ratings)</p>
                                    <p><strong>Reviews:</strong> {movie.review_count} reviews</p>
                                    <button
                                        onClick={() => handleWatchNow(movie)}
                                        style={{
                                            color: '#007bff',
                                            textDecoration: 'underline',
                                            background: 'none',
                                            border: 'none',
                                            cursor: 'pointer',
                                            fontSize: '16px'
                                        }}
                                    >
                                        Watch Now
                                    </button>
                                </div>
                            );
                        })}
                    </div>
                ) : (
                    !isLoading && !error && (
                        <p style={{ textAlign: 'center' }}>No movies found. Try searching for something else!</p>
                    )
                )}
            </section>

            <footer className="homepage-footer">
                <p>© 2024 Online Cinema. All rights reserved.</p>
            </footer>
        </div>
    );
}

export default HomePage;
