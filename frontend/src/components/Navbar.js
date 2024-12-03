import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';

function Navbar() {
    const location = useLocation();
    const navigate = useNavigate();
    const currentUser = authService.getCurrentUser();

    const handleLogout = () => {
        authService.logout();
        navigate('/login');
    };

    return (
        <nav className="bg-blue-500 p-4">
            <div className="container mx-auto flex justify-between items-center">
                <Link to="/" className="text-white text-xl font-bold">
                    AI Utdanningsassistent
                </Link>
                <div className="space-x-4">
                    {currentUser ? (
                        <>
                            <Link 
                                to="/education" 
                                className={`text-white hover:text-blue-100 ${
                                    location.pathname === '/education' ? 'font-bold' : ''
                                }`}
                            >
                                Utdanning
                            </Link>
                            <Link 
                                to="/entertainment" 
                                className={`text-white hover:text-blue-100 ${
                                    location.pathname === '/entertainment' ? 'font-bold' : ''
                                }`}
                            >
                                Underholdning
                            </Link>
                            <button 
                                onClick={handleLogout}
                                className="text-white hover:text-blue-100"
                            >
                                Logg ut ({currentUser.username})
                            </button>
                        </>
                    ) : (
                        <>
                            <Link 
                                to="/login" 
                                className={`text-white hover:text-blue-100 ${
                                    location.pathname === '/login' ? 'font-bold' : ''
                                }`}
                            >
                                Logg inn
                            </Link>
                            <Link 
                                to="/register" 
                                className={`text-white hover:text-blue-100 ${
                                    location.pathname === '/register' ? 'font-bold' : ''
                                }`}
                            >
                                Registrer deg
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
}

export default Navbar; 