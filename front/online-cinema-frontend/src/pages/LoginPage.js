import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import ErrorMessage from './ErrorMessage';

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

                // Если 400 Bad Request
                if (response.status === 400 && errorData.ditail) {
                    throw new Error(`${errorData.ditail.type}: ${errorData.ditail.message}`);
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
            setError({
                type: 'LoginError',
                message: err.message,
            });
            setSuccess(null);
        }
    };

    return (
        <div style={{ maxWidth: '500px', margin: '50px auto', textAlign: 'center', fontFamily: 'Arial, sans-serif' }}>
            {/* Заголовок */}
            <h1 style={{ marginBottom: '20px', color: '#333' }}>Вход</h1>

            {/* Сообщения об ошибке или успехе */}
            {error && <ErrorMessage type={error.type} message={error.message} />}
            {success && <p style={{ color: 'green', marginTop: '10px' }}>{success}</p>}

            {/* Форма логина */}
            <form
                onSubmit={handleSubmit}
                style={{
                    backgroundColor: '#f9f9f9',
                    padding: '20px',
                    borderRadius: '10px',
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                }}
            >
                <div style={{ marginBottom: '15px' }}>
                    <input
                        type="text"
                        placeholder="Имя пользователя или Email"
                        value={usernameOrEmail}
                        onChange={(e) => setUsernameOrEmail(e.target.value)}
                        style={inputStyle}
                        required
                    />
                </div>
                <div style={{ marginBottom: '15px' }}>
                    <input
                        type="password"
                        placeholder="Пароль"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={inputStyle}
                        required
                    />
                </div>
                <button type="submit" style={buttonStyle}>
                    Войти
                </button>
            </form>

            {/* Кнопка для перехода на страницу регистрации */}
            <div style={{ marginTop: '20px' }}>
                <p>Ещё нет аккаунта?</p>
                <Link to="/register" style={linkStyle}>
                    Перейти на страницу регистрации
                </Link>
            </div>
        </div>
    );
}

const inputStyle = {
    width: '100%',
    padding: '10px',
    fontSize: '16px',
    border: '1px solid #ccc',
    borderRadius: '5px',
    boxSizing: 'border-box',
};

const buttonStyle = {
    width: '100%',
    padding: '12px',
    fontSize: '16px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
};

const linkStyle = {
    color: '#007bff',
    textDecoration: 'none',
    fontWeight: 'bold',
    transition: 'color 0.3s',
};

export default LoginPage;
