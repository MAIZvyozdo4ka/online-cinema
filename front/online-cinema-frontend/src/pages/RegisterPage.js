import React, { useState } from 'react';
import ErrorMessage from './ErrorMessage';
import { Link } from 'react-router-dom';

function RegisterPage() {
    const [username, setUsername] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch(`${API_BASE_URL}/auth/registration`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username,
                    first_name: firstName,
                    last_name: lastName,
                    email,
                    password,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();

                // Обработка ошибки 400 (Bad Request)
                if (response.status === 400) {
                    throw new Error(`Error: ${errorData.ditail.message}`);
                }

                // Обработка ошибки 422 (Validation Error)
                if (response.status === 422) {
                    if (Array.isArray(errorData.detail)) {
                        const validationErrors = errorData.detail
                            .map((err) => err.msg)
                            .join(', ');
                        throw new Error(`Validation Error: ${validationErrors}`);
                    }
                    throw new Error('Validation error occurred, but no details were provided.');
                }

                // Обработка других ошибок
                throw new Error('Something went wrong. Please try again later.');
            }

            const data = await response.json();
            setSuccess('Registration successful!');
            setError(null);

            console.log('Response:', data);
        } catch (err) {
            setError(err.message);
            setSuccess(null);
        }
    };

    return (
        <div style={{ maxWidth: '500px', margin: '50px auto', textAlign: 'center', fontFamily: 'Arial, sans-serif' }}>
            <h1 style={{ marginBottom: '20px', color: '#333' }}>Регистрация</h1>

            {/* Сообщения об ошибках и успехе */}
            {error && <ErrorMessage type="ValidationError" message={error} />}
            {success && <p style={{ color: 'green', marginTop: '10px' }}>{success}</p>}

            {/* Форма регистрации */}
            <form onSubmit={handleSubmit} style={{ backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '10px', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)' }}>
                <div style={{ marginBottom: '15px' }}>
                    <input
                        type="text"
                        placeholder="Имя пользователя"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        style={inputStyle}
                        required
                    />
                </div>
                <div style={{ marginBottom: '15px' }}>
                    <input
                        type="text"
                        placeholder="Имя"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                        style={inputStyle}
                        required
                    />
                </div>
                <div style={{ marginBottom: '15px' }}>
                    <input
                        type="text"
                        placeholder="Фамилия"
                        value={lastName}
                        onChange={(e) => setLastName(e.target.value)}
                        style={inputStyle}
                        required
                    />
                </div>
                <div style={{ marginBottom: '15px' }}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
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
                    Зарегистрироваться
                </button>
            </form>

            {/* Кнопка для перехода на страницу логина */}
            <div style={{ marginTop: '20px' }}>
                <p>Уже есть аккаунт?</p>
                <Link to="/login" style={linkStyle}>
                    Перейти на страницу входа
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

export default RegisterPage;
