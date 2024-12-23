import React, { useState } from 'react';

function AdminRolesPage() {
    const [userId, setUserId] = useState('');
    const [role, setRole] = useState('user');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const handleSetRole = async (e) => {
        e.preventDefault();
        if (!userId || !role) {
            setError('Please provide both user ID and a role.');
            return;
        }

        setIsLoading(true);
        setError(null);
        setSuccessMessage(null);

        const bodyData = {
            user_id: parseInt(userId, 10),
            role
        };

        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/admin/set-role`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(bodyData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to set role');
            }

            setSuccessMessage(`Role updated successfully for user ${userId}`);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="homepage">
            <header className="homepage-header">
                <h1>User Role Management</h1>
            </header>

            {isLoading && <p style={{ textAlign: 'center', color: '#007bff' }}>Processing...</p>}
            {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
            {successMessage && <p style={{ color: 'green', textAlign: 'center' }}>{successMessage}</p>}

            <section style={{ marginTop: '20px', textAlign: 'center' }}>
                <h2>Set User Role</h2>
                <form onSubmit={handleSetRole} style={{ display: 'inline-block', textAlign: 'left' }}>
                    <div style={{ marginBottom: '10px' }}>
                        <label>User ID:</label><br/>
                        <input
                            type="number"
                            value={userId}
                            onChange={(e) => setUserId(e.target.value)}
                            style={{ width: '300px', padding: '5px' }}
                            required
                        />
                    </div>
                    <div style={{ marginBottom: '10px' }}>
                        <label>Role:</label><br/>
                        <select
                            value={role}
                            onChange={(e) => setRole(e.target.value)}
                            style={{ width: '300px', padding: '5px' }}
                        >
                            <option value="user">user</option>
                            <option value="moderator">moderator</option>
                            <option value="admin">admin</option>
                        </select>
                    </div>
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
                        Set Role
                    </button>
                </form>
            </section>

            <footer className="homepage-footer">
                <p>© 2024 Online Cinema. All rights reserved.</p>
            </footer>
        </div>
    );
}

export default AdminRolesPage;
