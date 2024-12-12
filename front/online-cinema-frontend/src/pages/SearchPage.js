import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SearchPage() {
    const [query, setQuery] = useState(''); // Строка поиска
    const [error, setError] = useState(null); // Ошибки запроса
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL; // URL API
    const navigate = useNavigate(); // Для перенаправления

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
                throw new Error(errorData.message || 'Search failed');
            }

            const results = await response.json();
            console.log('Search results:', results);
            // Здесь вы можете перенаправить на страницу с результатами или отобразить их на текущей
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Search</h1>
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
            {error && <p style={{ color: 'red', marginTop: '20px' }}>{error}</p>}
        </div>
    );
}

export default SearchPage;
