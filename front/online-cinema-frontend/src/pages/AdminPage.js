import React, { useEffect, useState } from 'react';
import './HomePage.css'; // Можно использовать тот же CSS или создать свой для AdminPage

function AdminPage() {
    const [movies, setMovies] = useState([]);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [currentMovie, setCurrentMovie] = useState({
        id: '',
        title: '',
        description: '',
        genres: '',
        imdb_link: '',
        tmbd_link: ''
    });

    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    // Загрузка списка фильмов при монтировании
    useEffect(() => {
        const fetchData = async () => {
            setIsLoading(true);
            setError(null);
            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/admin/moive`);
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || 'Failed to fetch movies');
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

        fetchData();
    }, [API_BASE_URL]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setCurrentMovie((prev) => ({
            ...prev,
            [name]: value
        }));
    };

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);

        const { id, title, description, genres, imdb_link, tmbd_link } = currentMovie;
        const movieData = {
            title,
            description,
            genres: genres.split(',').map((g) => g.trim()).filter(Boolean),
            links: {
                imdb_link,
                tmbd_link
            }
        };

        const method = id ? 'POST' : 'PUT';
        const endpoint = `${API_BASE_URL}/api/v1/admin/moive${id ? '' : ''}`;

        try {
            const response = await fetch(endpoint, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(id ? { ...movieData, id } : movieData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to save movie');
            }

            // После успешного добавления/обновления сбрасываем форму и обновляем список
            clearForm();
            // Повторная загрузка списка фильмов:
            await reloadMovies();
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const reloadMovies = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/admin/moive`);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to fetch movies');
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

    const handleEdit = (movie) => {
        setCurrentMovie({
            id: movie.id || '',
            title: movie.title || '',
            description: movie.description || '',
            genres: movie.genres ? movie.genres.join(', ') : '',
            imdb_link: movie.links?.imdb_link || '',
            tmbd_link: movie.links?.tmbd_link || ''
        });
    };

    const handleDelete = async (id) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/admin/moive/${id}`, {
                method: 'DELETE'
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to delete movie');
            }
            await reloadMovies();
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const clearForm = () => {
        setCurrentMovie({
            id: '',
            title: '',
            description: '',
            genres: '',
            imdb_link: '',
            tmbd_link: ''
        });
    };

    return (
        <div className="homepage">
            <header className="homepage-header">
                <h1>Admin Panel</h1>
                <p>Manage your movies here</p>
            </header>

            {isLoading && <p style={{ textAlign: 'center', color: '#007bff' }}>Processing...</p>}
            {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

            <section style={{ marginTop: '20px', textAlign: 'center' }}>
                <h2>{currentMovie.id ? 'Update Movie' : 'Add New Movie'}</h2>
                <form onSubmit={handleFormSubmit} style={{ display: 'inline-block', textAlign: 'left' }}>
                    <div style={{ marginBottom: '10px' }}>
                        <label>Title:</label><br/>
                        <input
                            type="text"
                            name="title"
                            value={currentMovie.title}
                            onChange={handleInputChange}
                            required
                            style={{ width: '300px', padding: '5px' }}
                        />
                    </div>
                    <div style={{ marginBottom: '10px' }}>
                        <label>Description:</label><br/>
                        <textarea
                            name="description"
                            value={currentMovie.description}
                            onChange={handleInputChange}
                            rows="3"
                            style={{ width: '300px', padding: '5px' }}
                        />
                    </div>
                    <div style={{ marginBottom: '10px' }}>
                        <label>Genres (comma separated):</label><br/>
                        <input
                            type="text"
                            name="genres"
                            value={currentMovie.genres}
                            onChange={handleInputChange}
                            style={{ width: '300px', padding: '5px' }}
                        />
                    </div>
                    <div style={{ marginBottom: '10px' }}>
                        <label>IMDb Link:</label><br/>
                        <input
                            type="url"
                            name="imdb_link"
                            value={currentMovie.imdb_link}
                            onChange={handleInputChange}
                            style={{ width: '300px', padding: '5px' }}
                        />
                    </div>
                    <div style={{ marginBottom: '10px' }}>
                        <label>TMDB Link:</label><br/>
                        <input
                            type="url"
                            name="tmbd_link"
                            value={currentMovie.tmbd_link}
                            onChange={handleInputChange}
                            style={{ width: '300px', padding: '5px' }}
                        />
                    </div>
                    <div style={{ marginBottom: '10px' }}>
                        <button
                            type="submit"
                            style={{
                                padding: '10px 20px',
                                fontSize: '16px',
                                backgroundColor: '#007bff',
                                color: '#fff',
                                border: 'none',
                                cursor: 'pointer',
                                marginRight: '10px'
                            }}
                        >
                            {currentMovie.id ? 'Update' : 'Add'}
                        </button>
                        {currentMovie.id && (
                            <button
                                type="button"
                                onClick={clearForm}
                                style={{
                                    padding: '10px 20px',
                                    fontSize: '16px',
                                    backgroundColor: 'gray',
                                    color: '#fff',
                                    border: 'none',
                                    cursor: 'pointer',
                                }}
                            >
                                Cancel
                            </button>
                        )}
                    </div>
                </form>
            </section>

            <section className="movie-results" style={{ marginTop: '40px' }}>
                <h2 style={{ textAlign: 'center' }}>Movies List</h2>
                {movies.length > 0 ? (
                    <div className="movie-list" style={{ textAlign: 'center', marginTop: '20px' }}>
                        {movies.map((movie) => (
                            <div key={movie.id} className="movie-item" style={{ border: '1px solid #ccc', marginBottom: '20px', padding: '10px', display: 'inline-block', width: '300px', verticalAlign: 'top', marginRight: '10px' }}>
                                <h3>{movie.title}</h3>
                                <p><strong>Description:</strong> {movie.description}</p>
                                <p><strong>Genres:</strong> {movie.genres.join(', ')}</p>
                                <p><strong>IMDb:</strong> <a href={movie.links?.imdb_link} target="_blank" rel="noopener noreferrer">{movie.links?.imdb_link}</a></p>
                                <p><strong>TMDB:</strong> <a href={movie.links?.tmbd_link} target="_blank" rel="noopener noreferrer">{movie.links?.tmbd_link}</a></p>
                                <div>
                                    <button
                                        onClick={() => handleEdit(movie)}
                                        style={{
                                            padding: '5px 10px',
                                            fontSize: '14px',
                                            backgroundColor: '#28a745',
                                            color: '#fff',
                                            border: 'none',
                                            cursor: 'pointer',
                                            marginRight: '5px'
                                        }}
                                    >
                                        Edit
                                    </button>
                                    <button
                                        onClick={() => handleDelete(movie.id)}
                                        style={{
                                            padding: '5px 10px',
                                            fontSize: '14px',
                                            backgroundColor: '#dc3545',
                                            color: '#fff',
                                            border: 'none',
                                            cursor: 'pointer'
                                        }}
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    !isLoading && !error && (
                        <p style={{ textAlign: 'center' }}>No movies found. Add a new one!</p>
                    )
                )}
            </section>

            <footer className="homepage-footer">
                <p>© 2024 Online Cinema Admin Panel. All rights reserved.</p>
            </footer>
        </div>
    );
}

export default AdminPage;
