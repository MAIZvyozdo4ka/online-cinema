import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
    return (
        <header style={headerStyle}>
            <Link to="/" style={logoStyle}>
                🎥 Кинотеатр
            </Link>
            <div>
                <Link to="/account" style={linkStyle}>
                    Профиль
                </Link>
            </div>
        </header>
    );
}

const headerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: '#fff',
    fontFamily: 'Arial, sans-serif',
};

const logoStyle = {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#fff',
    textDecoration: 'none',
};

const linkStyle = {
    color: '#fff',
    textDecoration: 'none',
    fontSize: '16px',
    fontWeight: 'bold',
};

export default Header;
