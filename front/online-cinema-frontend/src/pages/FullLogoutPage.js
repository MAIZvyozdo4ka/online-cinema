import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function FullLogoutPage() {
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
    const navigate = useNavigate();

    useEffect(() => {
        const fullLogout = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/me/full-logout`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    // Удаляем токены и перенаправляем
                    navigate('/');
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                } 
                if (response.status === 401) { //так себе затычка, но похуй
                    localStorage.removeItem('accessToken');
                    navigate('/login');
                    throw new Error('Unauthorized: Redirecting to login page');
                } else {
                    throw new Error('Failed to logout from all devices');
                }
            } catch (err) {
                console.error('Error during full logout:', err.message);
            }
        };

        fullLogout();
    }, [API_BASE_URL, navigate]);

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <p>Logging out from all devices...</p>
        </div>
    );
}

export default FullLogoutPage;
