import React, { useState } from 'react';
import './HomePage.css';

function HomePage() {
    const [searchQuery, setSearchQuery] = useState('');
    const [movies, setMovies] = useState([]);
    const [error, setError] = useState(null);
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const handleSearch = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${API_BASE_URL}/search?text=${encodeURIComponent(searchQuery)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to fetch movies');
            }

            const data = await response.json();
            setMovies(data);
            setError(null);
        } catch (err) {
            setError(err.message);
            setMovies([]);
        }
    };

    return (
        <div className="homepage">
            <header className="homepage-header">
                <h1>Search for Movies</h1>
                <form onSubmit={handleSearch}>
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
            </header>

            {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

            <section className="movie-results" style={{ marginTop: '20px' }}>
                {movies.length > 0 ? (
                    <div className="movie-list">
                        {movies.map((movie, index) => (
                            <div key={index} className="movie-item" style={{ marginBottom: '20px' }}>
                                <h2>{movie.title}</h2>
                                <p><strong>Genres:</strong> {movie.genres.join(', ')}</p>
                                <p><strong>Rating:</strong> {movie.rating} ({movie.rating_count} ratings)</p>
                                <p><strong>Reviews:</strong> {movie.review_count} reviews</p>
                                <a href={movie.local_link} style={{ color: '#007bff', textDecoration: 'underline' }}>
                                    Watch Now
                                </a>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p style={{ textAlign: 'center' }}>No movies found. Try searching for something else!</p>
                )}
            </section>

            <footer className="homepage-footer">
                <p>© 2024 Online Cinema. All rights reserved.</p>
            </footer>
        </div>
    );
}

export default HomePage;
