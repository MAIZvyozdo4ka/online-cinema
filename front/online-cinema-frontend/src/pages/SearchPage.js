import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SearchPage() {
    const [query, setQuery] = useState(''); 
    const [error, setError] = useState(null); 
    const [results, setResults] = useState([]); 
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL; 
    const navigate = useNavigate(); 

    const handleSearch = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/search?text=${encodeURIComponent(query)}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                },
            });

            if (response.status === 401) {
                // Удаляем токен и перенаправляем на логин
                localStorage.removeItem('accessToken');
                navigate('/login');
                return;
            }

            if (!response.ok) {
                const errorData = await response.json();
                if (errorData.type && errorData.message) {
                    throw { type: errorData.type, message: errorData.message };
                }
                throw { type: 'SEARCH_ERROR', message: 'Search failed.' };
            }

            const data = await response.json();
            setResults(data); 
            setError(null); 
        } catch (err) {
            setError({
                type: err.type || 'UNKNOWN_ERROR',
                message: err.message || 'An unexpected error occurred.',
            });
            setResults([]); 
        }
    };

    const handleRedirect = (movieId) => {
        const token = localStorage.getItem('accessToken');
        if (!token) {
            // Если нет авторизации, перенаправляем на логин
            navigate('/login');
            return;
        }
        // Переходим к фильму без /api/v1
        navigate(`/movie/${movieId}`); 
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Search</h1>
            {error && (
                <div style={{ color: 'red' }}>
                    {error.message}
                </div>
            )}
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter search query"
                style={{
                    padding: '10px',
                    width: '300px',
                    fontSize: '16px',
                }}
            />
            <button
                onClick={handleSearch}
                style={{
                    padding: '10px 20px',
                    fontSize: '16px',
                    backgroundColor: '#4CAF50',
                    color: '#fff',
                    border: 'none',
                    cursor: 'pointer',
                    marginLeft: '10px',
                }}
            >
                Search
            </button>

            <div style={{ marginTop: '20px' }}>
                {results.length > 0 ? (
                    results.map((movie) => {
                        // Извлекаем movieId из local_link
                        const movieId = movie.local_link ? movie.local_link.replace('/api/v1/movie/', '') : movie.id;

                        return (
                            <div key={movieId} style={{ marginBottom: '20px', textAlign: 'left', margin: '0 auto', width: '400px' }}>
                                <h3>{movie.title}</h3>
                                <p><strong>Genres:</strong> {movie.genres?.join(', ') || 'N/A'}</p>
                                <p><strong>Rating:</strong> {movie.rating || 'N/A'}</p>
                                {/* Кнопка "Watch Now" */}
                                <a
                                    href={`http://localhost:3000/movie/${movieId}`}
                                    style={{
                                        display: 'inline-block',
                                        padding: '10px 20px',
                                        fontSize: '14px',
                                        backgroundColor: '#007bff',
                                        color: '#fff',
                                        border: 'none',
                                        cursor: 'pointer',
                                        textDecoration: 'none'
                                    }}
                                >
                                    Watch Now
                                </a>
                            </div>
                        );
                    })
                ) : (
                    query && !error && <p>No movies found. Try a different query!</p>
                )}
            </div>
        </div>
    );
}

export default SearchPage;
