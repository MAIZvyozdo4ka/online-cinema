import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = ({ onLogout }) => {
  const isAuthenticated = !!localStorage.getItem('accessToken');

  return (
    <div className="home-page">
      <header>
        {isAuthenticated ? (
          <>
            <Link to="/search" className="home-button">К поиску фильмов</Link>
            <button onClick={onLogout} className="home-logout-button">Выйти</button>
          </>
        ) : (
          <Link to="/login" className="home-button">Войти</Link>
        )}
      </header>
      <main>
        <h1>MAIZvyozdo4ka</h1>
      </main>
    </div>
  );
};

export default HomePage;
