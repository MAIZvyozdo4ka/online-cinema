import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
    const [usernameOrEmail, setUsernameOrEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const navigate = useNavigate();

    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username_or_email: usernameOrEmail,
                    password,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();

                // Если 400 Bad Request с `type` и `message`
                if (response.status === 400) {
                    throw new Error(`Error: ${errorData.ditail.message}`);
                }

                // Если 422 Validation Error
                if (response.status === 422) {
                    if (Array.isArray(errorData.detail)) {
                        const validationErrors = errorData.detail
                            .map((err) => err.msg)
                            .join(', ');
                        throw new Error(`Validation Error: ${validationErrors}`);
                    }
                    throw new Error('Validation error occurred, but no details were provided.');
                }

                // Любая другая ошибка
                throw new Error('Failed to log in. Please try again later.');
            }

            const data = await response.json();
            setSuccess('Login successful!');
            setError(null);

            // Сохраняем токены в LocalStorage
            localStorage.setItem('accessToken', data.access_token);
            localStorage.setItem('refreshToken', data.refresh_token);

            console.log('Login Response:', data);
            navigate('/account');
        } catch (err) {
            setError(err.message);
            setSuccess(null);
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '50px auto', textAlign: 'center' }}>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '10px' }}>
                    <input
                        type="text"
                        placeholder="Username or Email"
                        value={usernameOrEmail}
                        onChange={(e) => setUsernameOrEmail(e.target.value)}
                        style={{
                            width: '100%',
                            padding: '10px',
                            fontSize: '16px',
                        }}
                        required
                    />
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
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
                        backgroundColor: '#28a745',
                        color: '#fff',
                        border: 'none',
                        cursor: 'pointer',
                    }}
                >
                    Login
                </button>
            </form>
            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
            {success && <p style={{ color: 'green', marginTop: '10px' }}>{success}</p>}
        </div>
    );
}

export default LoginPage;
