import React, { useEffect, useState } from 'react';

function ModeratorPage() {
    const [reviews, setReviews] = useState([]);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const [statementFilter, setStatementFilter] = useState('');
    const [limit, setLimit] = useState(250);
    const [offset, setOffset] = useState(0);

    const [deleteError, setDeleteError] = useState(null);
    const [deleteSuccess, setDeleteSuccess] = useState(null);

    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const fetchReviews = async () => {
        setIsLoading(true);
        setError(null);

        const params = new URLSearchParams();
        if (statementFilter) params.append('statement', statementFilter);
        params.append('limit', limit);
        if (offset) params.append('offset', offset);

        try {
            const response = await fetch(`${API_BASE_URL}/moderator/review/get-all?${params.toString()}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                }
            });

            if (response.status === 403) {
                // Недостаточно прав — incorrect_role
                const errorData = await response.json();
                throw new Error(errorData.message || 'Forbidden: You do not have the correct role.');
            }

            if (response.status === 401) {
                // Неавторизован — возможно токен истёк
                throw new Error('Not authorized. Please login again.');
            }

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to fetch reviews');
            }

            const data = await response.json();
            setReviews(data);
        } catch (err) {
            setError(err.message);
            setReviews([]);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchReviews();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [limit, offset, statementFilter]);

    const handleDelete = async (movie_id, user_id) => {
        setDeleteError(null);
        setDeleteSuccess(null);
        setIsLoading(true);

        try {
            const response = await fetch(`${API_BASE_URL}/moderator/review/delete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                },
                body: JSON.stringify({ movie_id, user_id })
            });

            if (response.status === 403) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Forbidden: You do not have the correct role.');
            }

            if (response.status === 401) {
                throw new Error('Not authorized. Please login again.');
            }

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to delete review');
            }

            setDeleteSuccess('Review successfully deleted!');
            // Обновить список рецензий
            fetchReviews();
        } catch (err) {
            setDeleteError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <header>
                <h1>Moderator Panel</h1>
                <p>Manage movie reviews here</p>
            </header>

            {isLoading && <p style={{ textAlign: 'center', color: '#007bff' }}>Processing...</p>}
            {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

            <section style={{ marginBottom: '20px' }}>
                <h2>Filter and Pagination</h2>
                <div style={{ display: 'flex', gap: '20px', marginBottom: '10px' }}>
                    <div>
                        <label>Statement Filter:</label><br/>
                        <select value={statementFilter} onChange={(e) => setStatementFilter(e.target.value)}>
                            <option value="">All</option>
                            <option value="positive">Positive</option>
                            <option value="negative">Negative</option>
                            <option value="neutral">Neutral</option>
                        </select>
                    </div>
                    <div>
                        <label>Limit (max 250):</label><br/>
                        <input
                            type="number"
                            value={limit}
                            onChange={(e) => setLimit(Number(e.target.value))}
                            style={{ width: '80px' }}
                            min={1}
                            max={250}
                        />
                    </div>
                    <div>
                        <label>Offset (max 10000000):</label><br/>
                        <input
                            type="number"
                            value={offset}
                            onChange={(e) => setOffset(Number(e.target.value))}
                            style={{ width: '80px' }}
                            min={0}
                            max={10000000}
                        />
                    </div>
                </div>
                <button onClick={fetchReviews} style={{ padding: '5px 10px', backgroundColor: '#007bff', color: '#fff', border: 'none', cursor: 'pointer' }}>
                    Apply Filters
                </button>
            </section>

            {deleteError && <p style={{ color: 'red', textAlign: 'center' }}>{deleteError}</p>}
            {deleteSuccess && <p style={{ color: 'green', textAlign: 'center' }}>{deleteSuccess}</p>}

            <section>
                <h2>Reviews List</h2>
                {reviews.length > 0 ? (
                    <table border="1" cellPadding="5" style={{ margin: '0 auto', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr>
                                <th>Movie ID</th>
                                <th>User ID</th>
                                <th>Header</th>
                                <th>Review</th>
                                <th>Statement</th>
                                <th>Last Modified</th>
                                <th>User Info</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {reviews.map((rev, index) => (
                                <tr key={index}>
                                    <td>{rev.movie_id}</td>
                                    <td>{rev.user && rev.user.user_id}</td>
                                    <td>{rev.header}</td>
                                    <td>{rev.review}</td>
                                    <td>{rev.statement}</td>
                                    <td>{rev.last_modified}</td>
                                    <td>{rev.user ? `${rev.user.username} (Role: ${rev.user.role})` : 'No user info'}</td>
                                    <td>
                                        <button
                                            onClick={() => handleDelete(rev.movie_id, rev.user.user_id)}
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
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    !error && !isLoading && <p style={{ textAlign: 'center' }}>No reviews found.</p>
                )}
            </section>
        </div>
    );
}

export default ModeratorPage;
