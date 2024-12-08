import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Education from './pages/Education';
import Entertainment from './pages/Entertainment';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import { authService } from './services/authService';

// 受保护的路由组件
const ProtectedRoute = ({ children }) => {
    try {
        const user = authService.getCurrentUser();
        if (!user) {
            return <Navigate to="/login" />;
        }
        return children;
    } catch (error) {
        console.error('Protected route error:', error);
        return <Navigate to="/login" />;
    }
};

function App() {
    return (
        <Router>
            <div className="App">
                <Navbar />
                <Routes>
                    <Route path="/" element={
                        authService.getCurrentUser() ? (
                            <Home />
                        ) : (
                            <Navigate to="/login" replace />
                        )
                    } />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route 
                        path="/education" 
                        element={
                            <ProtectedRoute>
                                <Education />
                            </ProtectedRoute>
                        } 
                    />
                    <Route 
                        path="/entertainment" 
                        element={
                            <ProtectedRoute>
                                <Entertainment />
                            </ProtectedRoute>
                        } 
                    />
                </Routes>
            </div>
        </Router>
    );
}

export default App; 