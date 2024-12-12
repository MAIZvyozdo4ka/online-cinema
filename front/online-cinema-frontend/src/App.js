import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RegisterPage from './pages/RegisterPage';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import UpdateTokensPage from './pages/UpdateTokensPage';
import AccountPage from './pages/AccountPage';
import LogoutPage from './pages/LogoutPage';
import FullLogoutPage from './pages/FullLogoutPage';
import MoviePage from './pages/MoviePage'; // Импорт страницы с информацией о фильме

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/update-tokens" element={<UpdateTokensPage />} />
                <Route path="/account" element={<AccountPage />} />
                <Route path="/logout" element={<LogoutPage />} />
                <Route path="/full-logout" element={<FullLogoutPage />} />
                <Route path="/movie/:movieId" element={<MoviePage />} /> {/* Новый маршрут для просмотра фильма */}
            </Routes>
        </Router>
    );
}

export default App;
