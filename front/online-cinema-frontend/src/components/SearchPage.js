import React, { useState } from 'react';
import './SearchPage.css';
import API_BASE_URL from '../config';

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [movies, setMovies] = useState([]);

  const handleSearch = () => {
    const token = localStorage.getItem('accessToken');
    fetch(`${API_BASE_URL}/search?query=${query}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      }
    })
    .then(response => {
      if (!response.ok) throw new Error('Ошибка поиска');
      return response.json();
    })
    .then(data => {
      setMovies(data);
    })
    .catch(error => {
      console.error('Ошибка поиска:', error);
    });
  };

  return (
    <div className="search-page">
      <div className="search-bar">
        <input
          type="text"
          placeholder="Введите название фильма"
          value={query}
          onChange={e => setQuery(e.target.value)}
          className="search-input"
        />
        <button onClick={handleSearch} className="search-button">Поиск</button>
      </div>

      <div className="movie-sections">
        <h2>Результаты поиска</h2>
        <div className="movie-cards">
          {movies.length > 0 ? (
            movies.map(movie => (
              <div className="movie-card" key={movie.id}>
                <img src={movie.posterUrl} alt={movie.title} className="movie-poster" />
                <div className="movie-info">
                  <h3>{movie.title}</h3>
                  <span className="movie-rating">{movie.rating}</span>
                </div>
              </div>
            ))
          ) : (
            <p className="no-movies">Фильмы не найдены</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchPage;
