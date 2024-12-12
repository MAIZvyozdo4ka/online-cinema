import React, { useState } from 'react';

function UpdateTokensPage() {
    const [refreshToken, setRefreshToken] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch(`${API_BASE_URL}/auth/update-tokens`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    refresh_token: refreshToken,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();

                // Обработка 302 Found
                if (response.status === 302 && errorData.ditail && errorData.ditail.message) {
                    throw new Error(`Error: ${errorData.ditail.message} (${errorData.ditail.type})`);
                }

                // Обработка 400 Bad Request
                if (response.status === 400 && errorData.ditail && errorData.ditail.message) {
                    throw new Error(`Error: ${errorData.ditail.message} (${errorData.ditail.type})`);
                }

                // Обработка 401 Unauthorized
                if (response.status === 401 && errorData.ditail && errorData.ditail.message) {
                    throw new Error(`Unauthorized: ${errorData.ditail.message}`);
                }

                // Любая другая ошибка
                throw new Error('Failed to update tokens. Please try again later.');
            }

            const data = await response.json();
            setSuccess('Tokens updated successfully!');
            setError(null);

            // Сохраняем токены
            localStorage.setItem('accessToken', data.access_token);
            localStorage.setItem('refreshToken', data.refresh_token);

            console.log('New Tokens:', data);
        } catch (err) {
            setError(err.message);
            setSuccess(null);
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '50px auto', textAlign: 'center' }}>
            <h1>Update Tokens</h1>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '10px' }}>
                    <input
                        type="text"
                        placeholder="Refresh Token"
                        value={refreshToken}
                        onChange={(e) => setRefreshToken(e.target.value)}
                        style={{
                            width: '100%',
                            padding: '10px',
                            fontSize: '16px',
                        }}
                        required
                    />
                </div>
                <button
                    type="submit"
                    style={{
                        width: '100%',
                        padding: '10px',
                        fontSize: '16px',
                        backgroundColor: '#007bff',
                        color: '#fff',
                        border: 'none',
                        cursor: 'pointer',
                    }}
                >
                    Update Tokens
                </button>
            </form>
            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
            {success && <p style={{ color: 'green', marginTop: '10px' }}>{success}</p>}
        </div>
    );
}

export default UpdateTokensPage;
