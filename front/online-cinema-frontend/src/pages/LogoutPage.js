import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function LogoutPage() {
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
    const navigate = useNavigate();

    useEffect(() => {
        const logout = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/me/logout`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                        'Content-Type': 'application/json',
                    },
                });

                // Проверяем статус ответа
                if (response.ok) {
                    navigate('/');
                    // Удаляем токены и перенаправляем
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                } 
                
                if (response.status === 401) {
                    localStorage.removeItem('accessToken');
                    navigate('/login');
                    throw new Error('Unauthorized: Redirecting to login page');
                } else {
                    throw new Error('Failed to logout');
                }
            } catch (err) {
                console.error('Error during logout:', err.message);
            }
        };

        logout();
    }, [API_BASE_URL, navigate]);

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <p>Logging out...</p>
        </div>
    );
}

export default LogoutPage;
